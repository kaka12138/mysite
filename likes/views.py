from django.shortcuts import render
from .models import LikeCount, LikeRecord
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist

def errorresponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)
    


def successreponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return errorresponse(400, '你未登陆')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        # 判断能否从ContentType获取对象
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return errorresponse(401, '对象不存在')


    # 处理数据
    if request.GET.get('is_like') == 'true':
        # 点赞
        liek_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 用户未点赞过,进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return successreponse(like_count.liked_num)
        else:
            # 已点赞过,不能重复点赞
            return errorresponse('402', '你已经点赞过')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点过赞,取消点赞
            liek_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            liek_record.delete()
            # 点赞总数减1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return successreponse(like_count.liked_num)
            else:
                # 点赞总数还为创建
                return errorresponse(404, '数据错误')
        else:
            # 没有点过赞, 不能取消
            return errorresponse(401, '你没有点赞过')