import typing as tp

from flask import Blueprint, jsonify, Response

from account.services_views import authenticate

video_urls = Blueprint('video', __name__, url_prefix='/api/video')


@video_urls.route('/', methods=['GET'])
@authenticate
def get_users() -> tp.Tuple[Response, int]:
    from video.models import Video
    # accounts, status_code = get_account()
    return jsonify({}), 200
