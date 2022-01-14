import typing as tp

from flask import Blueprint, Response, request
from flask_pydantic import validate

from utils.data_process import validate_data_for_create_or_update
from account.services_views import authenticate
from utils.endpoint_mixins import list_endpoint_mixin, detail_endpoint_mixin
from models import Video
from video.schemas import VideoDataUpdateView, VideoDataCreate

video_urls = Blueprint('video', __name__, url_prefix='/api/video')


@video_urls.route('/<int:pk>/', methods=['GET', 'PATCH', 'DELETE'])
@authenticate
def video_detail(pk: int) -> tp.Tuple[Response, int]:
    """
    Detail video
    """

    data = validate_data_for_create_or_update(schema=VideoDataUpdateView,
                                              request=request,
                                              read_only_fields=['account_id', 'bucket_path'])
    return detail_endpoint_mixin(schema=VideoDataUpdateView, model=Video, request=request, pk=pk, data=data)


@video_urls.route('/', methods=['GET', 'POST'])
@authenticate
def list_video() -> tp.Tuple[Response, int]:
    """
    List video
    """

    data = validate_data_for_create_or_update(schema=VideoDataCreate, request=request)
    data.update({'account_id': request.user.id})  # type: ignore
    return list_endpoint_mixin(schema=VideoDataCreate, model=Video, request=request, data=data)
