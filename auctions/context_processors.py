from .models import Category, Message

def categories_processor(request):
    return {
        'sidebar_categories': Category.objects.all()
    }

def unread_messages(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(recipient=request.user, read=False).count()
        return {'unread_count': unread_count}
    return {'unread_count': 0}
