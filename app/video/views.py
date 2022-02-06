import typing as tp

from flask import Blueprint, request

from utils.mixins import ListCreateViewMixin, RetrieveViewMixin

from models import Video, Account
from utils.permissions import IsAuthenticate

from video.permissions import IsAuthenticateCreateVideoPermission, IsOwnerOrReadOnlyVideoPermission
from video.serializer import VideoModelSerializer
from video.services_views import process_data_to_create_video

video_urls = Blueprint('video', __name__, url_prefix='/api/video')


class UserVideosView(ListCreateViewMixin):
    """
    Getting user videos
    """

    methods = ['GET']
    model = Video
    request = request
    search_fields = ['description', 'title']
    # TODO update according with soft delete
    # search_query = [Video.account_id == request.user.id]
    annotate_data = [
        {
            'model': Account,
            'annotate_fields': ['username']
        }
    ]
    serializer = VideoModelSerializer
    permission_classes = [IsAuthenticate]

    def update_search_query(self) -> None:
        self.search_query.append(Video.account_id == self.request.user.id)    # type: ignore


class VideoRetrieveView(RetrieveViewMixin):
    """
    View for getting or update or remove video using pk
    """

    methods = ['GET', 'PATCH', 'DELETE']
    model = Video
    request = request
    search_fields = ['description', 'title']
    # TODO update according with soft delete
    search_query = [Video.upload_date.is_not(None)]
    annotate_data = [
        {
            'model': Account,
            'annotate_fields': ['username']
        }
    ]
    serializer = VideoModelSerializer
    permission_classes = [IsOwnerOrReadOnlyVideoPermission]


class VideoListCreateView(ListCreateViewMixin):
    """
    View for getting all videos or create video
    """

    methods = ['GET', 'POST']
    model = Video
    request = request
    search_fields = ['description', 'title']
    # TODO update upload_date change to soft delete
    filter_query = [Video.upload_date.is_not(None)]
    annotate_data = [
        {
            'model': Account,
            'annotate_fields': ['username']
        }
    ]
    permission_classes = [IsAuthenticateCreateVideoPermission]
    serializer = VideoModelSerializer

    def perform_create_update(self, serializer_data: tp.Dict[str, tp.Union[str, int, bool]]) -> tp.Dict[
        str, tp.Union[str, int, bool]
    ]:
        serializer_data['account_id'] = self.request.user.id    # type: ignore

        bucket_path = process_data_to_create_video(request=self.request)
        serializer_data['bucket_path'] = bucket_path
        return serializer_data


video_urls.add_url_rule('/', view_func=VideoListCreateView.as_view('video_list'))
video_urls.add_url_rule('/<int:pk>/', view_func=VideoRetrieveView.as_view('video_retrieve'))
video_urls.add_url_rule('/user_videos/', view_func=UserVideosView.as_view('user_videos'))
