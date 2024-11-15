from django.http import StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Video, VideoTiming
from serverpart.models import Pack
from .services import open_file

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from user.permissions import HasAccessToVideo

class VideoDetailAPIView(APIView):
	permission_classes = [HasAccessToVideo]

	def get(self, request):
		pack_id = request.GET.get('pack_id')
		if not pack_id:
			return Response({"error": "pack_id not provided"}, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			
			video_id = Pack.objects.filter(pk=pack_id).values('video').first()
			if not video_id:
				return Response({"error": "No video found for the given pack_id"}, status=status.HTTP_404_NOT_FOUND)
			
			if not request.user.has_perm('view_video'):
				return Response({'error': 'Access denied. Subscription required.'}, status=status.HTTP_403_FORBIDDEN)

			video = Video.objects.get(pk=video_id['video'])

			video_data = {
					"id": video.id,
					"title": video.title,
					"description": video.description,
					"image_url": video.image.url,
					"created_at": video.create_at
			}
			return Response(video_data, status=status.HTTP_200_OK)

		except ObjectDoesNotExist:
			return Response({"error": "Invalid video or pack_id"}, status=status.HTTP_404_NOT_FOUND)

		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VideoStreamingAPIView(APIView):
	permission_classes = [HasAccessToVideo]
	def get(self, request):
		pk = request.GET.get('pack_id')
		if not pk:
				return Response({"detail": "pack_id not provided."}, status=400)

		try:
				video_id = Pack.objects.filter(pk=pk).values('video')
		except Video.DoesNotExist:
				return Response({"detail": "No Video matches the given query."}, status=404)
		file, status_code, content_length, content_range = open_file(request, video_id[0]['video'])
		response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
		response['Accept-Ranges'] = 'bytes'
		response['Content-Length'] = str(content_length)
		response['Cache-Control'] = 'no-cache'
		response['Content-Range'] = content_range
		response['Content-Disposition'] = 'inline'
		response['X-Content-Type-Options'] = 'nosniff'

		return response


class VideoTimingAPIView(APIView):
	permission_classes = [HasAccessToVideo]
	def get(self, request):
		pack_id = request.GET.get('pack_id')
		if not pack_id:
			return Response({"error": "pack_id not provided"}, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			timings = VideoTiming.objects.filter(video_id=Pack.objects.filter(pk=pack_id).values('video').first()['video'])
		except VideoTiming.DoesNotExist:
			return Response({'error': 'Timings not found'}, status=status.HTTP_404_NOT_FOUND)
		
		timing_dict = {timing.label: timing.time for timing in timings}
		return Response({ "timings" : timing_dict}, status=status.HTTP_200_OK)
