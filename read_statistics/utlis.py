from read_statistics.models import ReadNum
from django.contrib.contenttypes.models import ContentType


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):

        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # 计数加一
        readnum.read_num += 1
        readnum.save()
    return key