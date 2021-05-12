#include <iostream>
#include <cstdio>
extern "C"
{
	#include <libavcodec/avcodec.h>
	#include <libavformat/avformat.h>
	#include <libavutil/avutil.h>
}

#undef av_err2str
#define av_err2str(errnum) \
av_make_error_string((char*)__builtin_alloca(AV_ERROR_MAX_STRING_SIZE), AV_ERROR_MAX_STRING_SIZE, errnum)

static void encode(AVCodecContext* av_codec_context, AVFrame* frame, AVPacket* packet, FILE* file)
{
	int res;

	res = avcodec_send_frame(av_codec_context, frame);
	if (res < 0) {
		fprintf(stderr, "Unable to send frame for encoding.\n");
		exit(1);
	}

	while(res >= 0) {
		res = avcodec_receive_packet(av_codec_context, packet);

		// all packets sent
		if (res == AVERROR(EAGAIN) || res == AVERROR_EOF)
		{
			return;
		} else if (res < 0) {
			fprintf(stderr, "Error during encoding.\n");
			exit(1);
		}

		// printf("Encoded frame %3" PRId64 " (size=%5d)\n", packet->pts, packet->size);
		fwrite(packet->data, 1, packet->size, file);
		av_packet_unref(packet);
	}
}


int main()
{
	const char* filename = "tmp.mp4";

	AVOutputFormat* av_output_format = av_guess_format(NULL, filename, NULL);
	AVFormatContext* av_format_context;
	AVCodecContext* av_codec_context;
	AVCodec* av_codec;
	FILE* file;
  uint8_t endcode[] = { 0, 0, 1, 0xb7 };
	int res; //stores error codes (if returned);

	printf("Writing file with format %s (MIME type %s).\n", av_output_format->long_name, av_output_format->mime_type);

	av_codec = avcodec_find_encoder(av_output_format->video_codec);
	if (!av_codec) {
		fprintf(stderr, "Could not create video encoder.\n");
		exit(1);
	}

	av_codec_context = avcodec_alloc_context3(av_codec);
	if (!av_codec_context) {
		fprintf(stderr, "Could not create codec context.\n");
		exit(1);
	}

	AVFrame* frame = av_frame_alloc();
	if (!frame) {
		fprintf(stderr, "Frame failed allocation.\n");
		exit(1);
	}

	AVPacket* packet = av_packet_alloc();
	if (!packet) {
		fprintf(stderr, "Packet failed allocation.\n");
		exit(1);
	}

	av_codec_context->bit_rate = 4000000;
	av_codec_context->width = 1920;
	av_codec_context->height = 1080;
	// fps
	int fps = 60;
	av_codec_context->time_base = (AVRational){1,fps};
	av_codec_context->framerate = (AVRational){fps,1};

	av_codec_context->gop_size = fps*2; //one intra frame every 2 seconds
	av_codec_context->max_b_frames = 1; //max number of B-frames between normal frames
	av_codec_context->pix_fmt = AV_PIX_FMT_YUV420P; //color format

	//open codec
	if (avcodec_open2(av_codec_context, av_codec, NULL) < 0) {
		fprintf(stderr, "Could not open codec.\n");
		exit(1);
	}

	file = fopen(filename, "wb");
	if (!file) {
		fprintf(stderr, "Could not open file: %s\n", filename);
		exit(1);
	}

	frame->format = av_codec_context->pix_fmt;
	frame->width = av_codec_context->width;
	frame->height = av_codec_context->height;

	res = av_frame_get_buffer(frame, 32);

	for (int i = 0; i < fps*60; i++) { //encode 60 seconds of video
		// fflush(stdout);

		res = av_frame_make_writable(frame); // make frame writable
		if (res < 0)
			exit(1);

		//create dummy frame
		for(int y = 0; y < frame->height; y++) {
			for(int x = 0; x < frame->width; x++) {
				frame->data[0][y * frame->linesize[0] + x] = x + y + i * 3;
			}
		}

		//Cb and Cr
		for(int y = 0; y < frame->height/2; y++) {
			for(int x = 0; x < frame->width/2; x++) {
				frame->data[1][y * frame->linesize[1] + x] = y + i;
				frame->data[2][y * frame->linesize[2] + x] = x + i;
			}
		}

		frame->pts = i;

		//encode image
		encode(av_codec_context, frame, packet, file);
	}

	//flush encoder
	encode(av_codec_context, NULL, packet, file);

	//write file end code
	fwrite(endcode, 1, sizeof(endcode), file);
	fclose(file);

	avcodec_free_context(&av_codec_context);
	av_frame_free(&frame);
	av_packet_free(&packet);

	return 0;
}