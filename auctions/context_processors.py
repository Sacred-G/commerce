from .models import Category, Message
from .views import get_recent_activities


def categories_processor(request):
    return {
        'sidebar_categories': Category.objects.all()
    }


def unread_messages(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(
            recipient=request.user, read=False).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0}


def recent_activities(request):
    if request.user.is_authenticated:
        activities = get_recent_activities(request.user)
        return {'recent_activities': activities}
    return {'recent_activities': []}
