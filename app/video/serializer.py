from models import Video

from utils.serializers import BaseModelSerializer


class VideoModelSerializer(BaseModelSerializer):
    """
    Model serializer for model video
    """

    read_only_fields = ['id', 'bucket_path', 'upload_date', 'account_id']
    model = Video
