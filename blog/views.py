from django.shortcuts import render
from .models import Post


def home(request):
    """Home"""

    context = {
        "posts": Post.objects.all(),
    }

    return render(request, "blog/home.html", context)


def about(request):
    """About"""

    return render(request, "blog/about.html")
