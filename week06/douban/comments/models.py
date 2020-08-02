from django.db import models

class Comments(models.Model):
    field_id = models.CharField(db_column='_id', primary_key=True, max_length=64)
    comment_info = models.CharField(max_length=10240, blank=True, null=True)
    comment_time = models.CharField(max_length=32, blank=True, null=True)
    crawl_time = models.CharField(max_length=32, blank=True, null=True)
    movie_id = models.CharField(max_length=32, blank=True, null=True)
    movie_name = models.CharField(max_length=32, blank=True, null=True)
    nickname = models.CharField(max_length=32, blank=True, null=True)
    rating_star = models.CharField(max_length=8, blank=True, null=True)
    rating_type = models.CharField(max_length=8, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)
    user_id = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'
