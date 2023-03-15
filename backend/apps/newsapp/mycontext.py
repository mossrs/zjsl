from .models import NewsChannel, Comment


def get_channels(request):
    """
        获取导航信息
    """
    channels = NewsChannel.objects.order_by('-id')
    return {'channels': channels}


def get_comment(request):
    comments = Comment.objects.order_by('-id')
    return {'comments': comments}