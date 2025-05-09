from .models import Video, VideoTiming
from serverpart.models import Pack
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from user.permissions import get_user_active_access_rights


class VideoDetailAPIView(APIView):
    def get(self, request):
        pack_id = request.GET.get('pack_id')
        if not pack_id:
            return Response({"error": "pack_id not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            video_id = Pack.objects.filter(pk=pack_id).values('video').first()
            if not video_id or not video_id['video']:
                return Response({"error": "No video found for this pack_id"},
                                status=status.HTTP_404_NOT_FOUND)

            video = Video.objects.prefetch_related(
                'access_rights').get(pk=video_id['video'])

            video_rights = set(video.access_rights.all())
            user_rights = set(get_user_active_access_rights(request.user))

            if not user_rights & video_rights:
                return Response({"error": "Access denied"},
                                status=status.HTTP_403_FORBIDDEN)

            video_data = {
                "id": video.id,
                "title": video.title,
                "description": video.description,
                "image_url": video.image.url if video.image else None,
                "video_url": video.file_url,
                "created_at": video.create_at
            }
            return Response(video_data, status=status.HTTP_200_OK)

        except Video.DoesNotExist:
            return Response({"error": "Invalid video or pack_id"},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VideoTimingAPIView(APIView):
    def get(self, request):
        video_id = request.GET.get('video_id')
        if not video_id:
            return Response({"error": "video_id not provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.prefetch_related(
                'access_rights').get(pk=video_id)

            user_rights = set(get_user_active_access_rights(request.user))
            video_rights = set(video.access_rights.all())

            if not user_rights & video_rights:
                return Response({"error": "Access denied"},
                                status=status.HTTP_403_FORBIDDEN)

            timings = VideoTiming.objects.filter(video=video)
            timing_dict = {timing.label: timing.time for timing in timings}
            return Response({"timings": timing_dict}, status=status.HTTP_200_OK)

        except Video.DoesNotExist:
            return Response({"error": "Invalid video_id"},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
