# blog/forms.py
from django import forms
from .models import Post, Comment, HashTag

# Form : html에 있는 form태그
# forms.Form 일반폼 
# Model Form : 모델(Model)과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있는 폼
# forms.ModelForm
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post # 사용할 모델
        # PostForm에서 사용 할 Post 모델의 속성
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'cols':'35'}),
        }
        
        labels = {
            'title' : '제목',
            'content' : '내용',
        }
# 즉, PostForm은 Post모델과 연결된 폼이고 Post모델의 title과 content를 사용 한다고 정의

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
    