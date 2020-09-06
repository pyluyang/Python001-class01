# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Article(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=16, blank=True, null=True)
    mall = models.CharField(max_length=255, blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    spider_name = models.CharField(max_length=32, blank=True, null=True)
    crawl_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article'


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    article_id = models.CharField(max_length=32, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=32, blank=True, null=True)
    user_url = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=8, blank=True, null=True)
    pub_time = models.CharField(max_length=64, blank=True, null=True)
    come_from = models.CharField(max_length=64, blank=True, null=True)
    comment_id = models.CharField(max_length=32, blank=True, null=True)
    comment_info = models.CharField(max_length=10240, blank=True, null=True)
    comment_quote_id = models.CharField(max_length=32, blank=True, null=True)
    spider_name = models.CharField(max_length=32, blank=True, null=True)
    crawl_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)
    goods_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class Sentiments(models.Model):
    id = models.TextField(primary_key=True)
    article_id = models.TextField(blank=True, null=True)
    goods_type = models.TextField(blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    pub_time = models.TextField(blank=True, null=True)
    comment_id = models.TextField(blank=True, null=True)
    comment_info = models.TextField(blank=True, null=True)
    crawl_time = models.TextField(blank=True, null=True)
    sentiments = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sentiments'
