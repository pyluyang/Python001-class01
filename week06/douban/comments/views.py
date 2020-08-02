import json

from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpResponseNotFound
from .models import Comments

@require_GET
def index(request):
    limit = 200
    keys = ('movie_name', 'rating_star', 'comment_info', 'comment_time')
    try:
        results = list(Comments.objects.filter(rating_star__gt=3, movie_name='肖申克的救赎').values(*keys)[:limit])
        return render(request, 'comments/index.html', {'results': json.dumps(results, ensure_ascii=False)})
    except Exception as e:
        return HttpResponseNotFound(f"<h1>{e}</h1>")
