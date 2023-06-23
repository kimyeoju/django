from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True) # 초기값
    updated_at = models.DateTimeField(auto_now=True) # 수정할때마다 바뀜


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # 위의 Post를 연결하는 관계 데이터베이스 on_delete를 하면 Post에서 model이 사라지면 comment에서도 사라진다 Post:Comment --> '1:N의 관계'표현 
    content = models.TextField()
    writer = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment on {self.post.title}'
    
    
class HashTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name