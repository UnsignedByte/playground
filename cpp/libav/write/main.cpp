#include <iostream>
#include <cstdio>
extern "C"
{
	#include <libavcodec/avcodec.h>
	#include <libavformat/avformat.h>
	#include <libavutil/avutil.h>
	#include <libavformat/avio.h>
}

#undef av_err2str
#define av_err2str(errnum) \
av_make_error_string((char*)__builtin_alloca(AV_ERROR_MAX_STRING_SIZE), AV_ERROR_MAX_STRING_SIZE, errnum)

static int write_frame(AVFormatContext* av_format_context, const AVRational& time_base, AVStream *av_stream, AVPacket *packet)
{
	/* rescale output packet timestamp values from codec to stream timebase */
	av_packet_rescale_ts(packet, time_base, av_stream->time_base);
	packet->stream_index = av_stream->index;
	printf("Stream Index: %d, PTS: %" PRId64 ", DTS: %" PRId64 ", pos: %" PRId64 ", duration: %" PRId64 "\n", packet->stream_index, packet->pts, packet->dts, packet->pos, packet->duration);
	return av_interleaved_write_frame(av_format_context, packet);
}

static void encode(AVFormatContext* av_format_context, AVCodecContext* av_codec_context, AVStream* av_stream, AVFrame* frame, AVPacket* packet)
{
	int res;

	res = avcodec_send_frame(av_codec_context, frame);
	if (res < 0) {
		fprintf(stderr, "Unable to send frame for encoding.\n");
		exit(1);
	}

	while(1) {
		res = avcodec_receive_packet(av_codec_context, packet);

		// all packets sent
		if (res == AVERROR(EAGAIN) || res == AVERROR_EOF)
		{
			// av_packet_free(&packet);
			break;
		} else if (res < 0) {
			fprintf(stderr, "Error during encoding.\n");
			exit(1);
		}

		// packet->pts = pts;
		packet->duration = 1;
		// printf("%ld\n", packet->duration);

		res = write_frame(av_format_context, av_codec_context->time_base, av_stream, packet);
		if (res < 0) {
			fprintf(stderr, "Error muxing packet\n");
			break;
		}
		av_packet_unref(packet);
	}
}


int main()
{
	const char* filename = "tmp.mp4";

	AVFormatContext* av_format_context;
	AVCodecContext* av_codec_context;
	AVCodec* av_codec;
	AVStream* av_stream;
  uint8_t endcode[] = { 0, 0, 1, 0xb7 };
	int res; //stores error codes (if returned);

	av_format_context = avformat_alloc_context();
	if (!av_format_context) {
		fprintf(stderr, "Could not allocate format context.\n");
		exit(1);
	}

	res = avformat_alloc_output_context2(&av_format_context, av_guess_format(NULL, filename, NULL), NULL, filename);
	if (res < 0){
		printf("Setting output format failed with code %s\n", av_err2str(res));
		exit(1);
	}

	printf("Writing file with format %s (MIME type %s).\n", av_format_context->oformat->long_name, av_format_context->oformat->mime_type);

	av_codec = avcodec_find_encoder(av_format_context->oformat->video_codec);
	if (!av_codec) {
		fprintf(stderr, "Could not create video encoder.\n");
		exit(1);
	}

	av_codec_context = avcodec_alloc_context3(av_codec);
	if (!av_codec_context) {
		fprintf(stderr, "Could not create codec context.\n");
		exit(1);
	}

	av_stream = avformat_new_stream(av_format_context, av_codec);
	if (!av_stream) {
		fprintf(stderr, "Could not create AVStream.\n");
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

	av_codec_context->width = 800;
	av_codec_context->height = 600;
	av_codec_context->bit_rate = av_codec_context->width*av_codec_context->height*4;
	// fps
	const int fps = 30;
	av_codec_context->time_base = (AVRational){1,fps};
	av_codec_context->framerate = (AVRational){fps,1};

	av_codec_context->gop_size = fps; // intra frames
	av_codec_context->max_b_frames = 1; //max number of B-frames between normal frames
	av_codec_context->pix_fmt = AV_PIX_FMT_YUV420P; //acolor format

	frame->format = av_codec_context->pix_fmt;
	frame->width = av_codec_context->width;
	frame->height = av_codec_context->height;

	av_stream->r_frame_rate = av_codec_context->framerate;
	av_stream->avg_frame_rate = av_codec_context->framerate;
	av_stream->time_base = av_codec_context->time_base;

	//open codec
	if (avcodec_open2(av_codec_context, av_codec, NULL) < 0) {
		fprintf(stderr, "Could not open codec.\n");
		exit(1);
	}

	// av_stream->codec = av_codec_context;

	res = avcodec_parameters_from_context(av_stream->codecpar, av_codec_context);
	if (res < 0) {
		fprintf(stderr, "Failed to get avcodec params; Error code '%s'", av_err2str(res));
    exit(1);
	}

	res = avio_open(&av_format_context->pb, filename, AVIO_FLAG_WRITE); // open output file
	if (res < 0) {
    fprintf(stderr, "Could not open output file '%s'", filename);
    exit(1);
	}

	AVDictionary* av_opts = NULL;
	av_dict_set(&av_opts, "movflags", "frag_keyframe+empty_moov+default_base_moof", 0);

	res = avformat_write_header(av_format_context, &av_opts);
	if (res < 0) {
		fprintf(stderr, "Writing video header fails with code %s.\n", av_err2str(res));
		exit(1);
	}

	res = av_frame_get_buffer(frame, 32);

	for (int i = 0; i < fps*60; i++) { //encode 60 seconds of video
		fflush(stdout);

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
				frame->data[1][y * frame->linesize[1] + x] = x + i * 2;
				frame->data[2][y * frame->linesize[2] + x] = y + i * 5;
			}
		}

		// frame->pts = av_rescale_q(i, av_codec_context->time_base, av_stream->time_base);
		frame->pts = i;

		//encode image
		encode(av_format_context, av_codec_context, av_stream, frame, packet);
	}

	//flush encoder
	encode(av_format_context, av_codec_context, av_stream, NULL, packet);

	//write file end code
	res = av_write_trailer(av_format_context);
	if (res < 0) {
		fprintf(stderr, "Writing video trailer fails with code %s.\n", av_err2str(res));
		exit(1);
	}

	printf(
		"\nCodec Parameters:\n"
		"Video size: %dx%d\n" 
		"Time base: %d/%d, Framerate: %d/%d\n"
		"\nStream Parameters:\n"
		"Time base: %d/%d\n"
		"Real Framerate: %d/%d\n"
		"Average Framerate: %d/%d\n"
		"Duration: %" PRId64 "\n"
		"Num frames: %" PRId64 "\n",
		av_codec_context->width, av_codec_context->height,
		av_codec_context->time_base.num, av_codec_context->time_base.den,
		av_codec_context->framerate.num, av_codec_context->framerate.den,
		av_stream->time_base.num, av_stream->time_base.den,
		av_stream->r_frame_rate.num, av_stream->r_frame_rate.den,
		av_stream->avg_frame_rate.num, av_stream->avg_frame_rate.den,
		av_stream->duration, av_stream->nb_frames
		);

	avcodec_free_context(&av_codec_context);
	av_frame_free(&frame);
	av_packet_free(&packet);

	return 0;
}