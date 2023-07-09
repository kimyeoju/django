from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

class IndexMain(View):
    def get(self,request):
        context = {
            'title': 'Index'
        }
        return render(request, 'index.html', context)
    # 여기서 주의할건 파일 안에 들어가 있는 템플릿이 아니니까
    # user/user_register.html 이라고 쓸 필요가 없다.