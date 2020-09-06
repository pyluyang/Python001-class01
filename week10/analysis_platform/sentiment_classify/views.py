import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Article, Sentiments


def index(request, *args, **kwargs):
    try:
        article = Article.objects.filter(position__lte=39).values('id', 'title', 'url', 'mall', 'position')
        article = {i.pop('id'): i for i in article}
        sentiments = Sentiments.objects.values()
        sentiments = [{**i, **article[i['article_id']]} for i in sentiments if i['article_id'] in article]
        keys = {
            'comment_id': 'ID',
            'goods_type': '商品',
            'mall': '商城',
            'position': '商品排名',
            'comment_info': '评论内容',
            'sentiments': '情感倾向',
            'url': 'URL',
        }
        context = {
            'results': json.dumps(sentiments, ensure_ascii=False),
            'keys': json.dumps(keys, ensure_ascii=False),
        }
        return render(request, 'index.html', context)
    except Exception as e:
        return HttpResponseNotFound(f"<h1 style='color:red'>{e}</h1>")
