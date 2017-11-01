from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), verbose_name='creator')
    title = models.CharField(max_length=255)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    is_publish = models.BooleanField(default=False)

    class Meta:
        db_table = 'Posts'
        verbose_name_plural = 'All posts'
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def change_post_update_date(self):
        self.date_updated = timezone.now()

    def user_is_owner(self, user):
        if user.id == self.author_id:
            return True
        return False

