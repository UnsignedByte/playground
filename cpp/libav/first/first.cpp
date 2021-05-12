#include <iostream>
extern "C"
{
	#include <libavcodec/avcodec.h>
	#include <libavformat/avformat.h>
	#include <libavutil/avutil.h>
}

#undef av_err2str
#define av_err2str(errnum) \
av_make_error_string((char*)__builtin_alloca(AV_ERROR_MAX_STRING_SIZE), AV_ERROR_MAX_STRING_SIZE, errnum)

int main()
{
	const char* filename = "../videos/processor_burning.avi";

	AVFormatContext* fctx = avformat_alloc_context();

	if (!fctx) {
		printf("Could't create Format Context\n");
		return 0;
	}

	int resp = avformat_open_input(&fctx, filename, nullptr, nullptr);
	if (resp < 0) {
		printf("avformat_open_input fails with code %s.\n", av_err2str(resp));
		return 0;
	}

	int video_stream_index = -1;
	AVCodec* avcodec;
	AVCodecParameters* avcodecparams;

	for(int i = 0; i < fctx->nb_streams; i++)
	{
		AVStream* stream = fctx->streams[i];

		avcodecparams = stream->codecpar;
		avcodec = avcodec_find_decoder(avcodecparams->codec_id);

		if (!avcodec)
		{
			printf("Couldn't locate decoder for stream %d.\n", i);
			continue;
		}

		if(avcodecparams->codec_type == AVMEDIA_TYPE_VIDEO) {
			video_stream_index = i;
			printf("Located video stream at stream index %d\n",video_stream_index);
			break;
		}
	}

	if (video_stream_index == -1){
		printf("Couldn't find valid video stream in file.\n");
		return 0;
	}

	// Set up codec context
	AVCodecContext* cctx = avcodec_alloc_context3(avcodec);

	if (!cctx) {
		printf("Couldn't create codec context.\n");
		return 0;
	}

	if (avcodec_parameters_to_context(cctx, avcodecparams) < 0)
	{
		printf("Couldn't initialize av codec context\n");
		return 0;
	}

	if (avcodec_open2(cctx, avcodec, NULL) < 0) {
		printf("Couldn't open codec\n");
		return 0;
	}

	AVFrame* av_frame = av_frame_alloc();
	if (!av_frame) {
		printf("Couldn't allocate frame\n");
		return 0;
	}

	AVPacket* av_packet = av_packet_alloc();
	if (!av_packet) {
		printf("Couldn't allocate packet\n");
		return 0;
	}

	//Read through each packet until we get one we want

	while (av_read_frame(fctx, av_packet) >= 0) {
		if (av_packet->stream_index != video_stream_index) { //Not a video frame
			continue;
		}

		resp = avcodec_send_packet(cctx, av_packet);
		if (resp < 0) {
			printf("Failed to decode packet: %s\n", av_err2str(resp));
			return 0;
		}
		resp = avcodec_receive_frame(cctx, av_frame);
		if (resp == AVERROR(EAGAIN) || resp == AVERROR_EOF) {
			continue;
		}
		if (resp < 0) {
			printf("Failed to decode packet: %s\n", av_err2str(resp));
			return 0;
		}

		av_packet_unref(av_packet);
		break;
	}

	unsigned char* data = new unsigned char[av_frame->width*av_frame->height*3];

	avformat_close_input(&fctx);
	avformat_free_context(fctx);
	av_frame_free(&av_frame);
	av_packet_free(&av_packet);
	avcodec_free_context(&cctx);
	return 0;
}