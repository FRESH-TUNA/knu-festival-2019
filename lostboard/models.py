import os
from django.db import models
from django.conf import settings

class Post(models.Model):
    content = models.TextField(null=False)
    image = models.ImageField(null=True, upload_to="lostpost")
    found = models.BooleanField(default=False)      # 주웠어요=True, 잃어버렸어요=False
    password = models.CharField(null=False, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return ("{}").format(self.content)

    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Post, self).delete(*args, **kargs)

class Comment(models.Model):
    post = models.ForeignKey(
        'Post', 
        on_delete=models.CASCADE, 
        related_name='comments', 
        blank=True,
    )
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='parent_comments', null=True)
    content = models.TextField(null=False)
    # depth를 제한할 필요성이 있을때 사용한다.
    active = models.BooleanField(default=True)
    depth = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=50)
