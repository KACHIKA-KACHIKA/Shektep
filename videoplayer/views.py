from django.core.exceptions import ObjectDoesNotExist
from .models import Video, VideoTiming
from serverpart.models import Pack
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from user.permissions import HasAccessToVideo


class VideoDetailAPIView(APIView):
    permission_classes = [HasAccessToVideo]

    def get(self, request):
        pack_id = request.GET.get('pack_id')
        if not pack_id:
            return Response({"error": "pack_id not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            video_id = Pack.objects.filter(pk=pack_id).values('video').first()
            if not video_id:
                return Response({"error": "No video found for this pack_id"},
                                status=status.HTTP_404_NOT_FOUND)

            video = Video.objects.get(pk=video_id['video'])

            video_data = {
                "id": video.id,
                "title": video.title,
                "description": video.description,
                "image_url": video.image.url,
                "video_url": video.file_url,
                "created_at": video.create_at
            }
            return Response(video_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"error": "Invalid video or pack_id"},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VideoTimingAPIView(APIView):
    permission_classes = [HasAccessToVideo]

    def get(self, request):
        video_id = request.GET.get('video_id')
        if not video_id:
            return Response({"error": "video_id not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            timings = VideoTiming.objects.filter(video_id=video_id)
        except VideoTiming.DoesNotExist:
            return Response({'error': 'Timings not found'},
                            status=status.HTTP_404_NOT_FOUND)

        timing_dict = {timing.label: timing.time for timing in timings}
        return Response({"timings": timing_dict}, status=status.HTTP_200_OK)
