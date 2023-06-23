# blog/forms.py
from django import forms
from .models import Post, Comment, HashTag

# Form : html에 있는 form태그
# Model Form : model을 사용하는 form
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
        # 이 fields만 받을거야 ! 
        widgets = {
            'content' : forms.Textarea(attrs={'rows': '5', 'cols':'35'})
        }
        # widgets는 content를 보여주겠다! 라는 함수
        # attrs는 태그 속성이다 html에 있는 태그만 바꿀 수 있다.
        

class HashTagForm(forms.ModelForm):
    
    class Meta:
        model = HashTag
        fields = ['name']
        # 사용자에게 값을 가져와야함
    