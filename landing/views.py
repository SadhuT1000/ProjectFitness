from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render
from courses.models import Course, Stream


from django.conf import settings
from courses.models import Course, Stream
from django.shortcuts import render

def home(request):
    """Главная страница с курсами и потоками"""
    courses = Course.objects.filter(is_published=True)
    streams = Stream.objects.filter(status='open')

    context = {
        "courses": courses,
        "streams": streams,
        "media_url": settings.MEDIA_URL,  # добавляем MEDIA_URL в контекст
    }

    return render(request, "landing/home.html", context)


def privacy(request):
    """Статичные страницы"""
    return render(request, "landing/privacy.html")

def terms(request):
    return render(request, "landing/terms.html")

