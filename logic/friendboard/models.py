from django.db import models

# Create your models here.
class Post(models.Model):
    content = models.TextField(default='')             # 길이 제한이 없는 문자열
    created_at = models.DateTimeField(auto_now_add=True) # 해당 레코드 생성시 현재 시간 자동저장
    password = models.CharField(max_length=50)

    class Meta:
        ordering=['-created_at']
        
    def __str__ (self):
        return self.content
    
    def root_comments(self):
        return self.comments.filter(parent__isnull=True).all()

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='parent_comments', null=True)
    # depth를 제한할 필요성이 있을때 사용한다.
    depth = models.IntegerField(default=0)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def overview(self):
        if len(self.content) > 10:
            return "{}...".format(self.content[:10])
        else:
            return self.content