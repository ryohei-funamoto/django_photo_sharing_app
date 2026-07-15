from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', default='images/noimage.png')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.title
