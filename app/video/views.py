from flask import Blueprint, request

from utils.mixins import ListCreateViewMixin

from models import Video, Account

from video.serializer import VideoModelSerializer
from video.services_views import process_data_to_create_video

from utils.serializers import serializer_data_type

video_urls = Blueprint('video', __name__, url_prefix='/api/video')


class VideoListCreateView(ListCreateViewMixin):
    """
    View for getting all videos or create video
    """

    methods = ['GET', 'POST']
    model = Video
    request = request
    search_fields = ['description', 'title']
    # TODO update upload_date change to soft delete(Only for show)
    filter_query = [Video.upload_time.is_not(None)]
    annotate_data = [
        {
            'model': Account,
            'annotate_fields': ['username']
        }
    ]
    serializer = VideoModelSerializer

    def perform_create(self, serializer_data: serializer_data_type) -> serializer_data_type:
        serializer_data['bucket_path'] = process_data_to_create_video(request=self.request)
        serializer_data['account_id'] = self.request.user.id  # type: ignore
        return serializer_data


video_urls.add_url_rule('/', view_func=VideoListCreateView.as_view('video_list'))
