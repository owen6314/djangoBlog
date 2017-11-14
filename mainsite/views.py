from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'blog/index.html', context={
            'title': '首页',
            'welcome': 'welcome'
        }')
