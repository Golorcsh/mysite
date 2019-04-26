from read_statistics.models import ReadNum
from django.contrib.contenttypes.models import ContentType


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 总阅读数量+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

    return key


