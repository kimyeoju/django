from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Post, Comment, HashTag
from .forms import PostForm, CommentForm, HashTagForm
from django.urls import reverse_lazy, reverse

# # Create your views here.
# def index(request):
#     if request.method == 'GET':
#         return HttpResponse('Index page GET')
#     # 나머지 요청
#     # 에러, 예외처리
#     return HttpResponse('No!!!')


### Post
# 게시판 목록 조회
# view 클래스 / HTTP 요청방식 (GET, POST)따라 처리하는 메서드
class Index(View):
    def get(self, request):
        # return HttpResponse('Index page GET class')
        
        # 데이터베이스에 접근해서 값을 가져와야 합니다.
        # 게시판에 글들을 보여줘야하기 때문에 데이터베이스(models.py)에서 "값 조회"
        # Mymodel.objects.all()
        post_objs = Post.objects.all()
        # 값을 계속해서 사용할 땐 변수를 할당하는 것이 좋다.
        # context = 데이터베이스에서 가져온 값
        context = {
            "posts": post_objs
        }
        # print(post_objs) -> 콘솔에서 확인용 Queryset[post 1,2,3,4,5] -> 리스트 객체이기 때문에 순회 가능 
        return render(request, 'blog/post_list.html', context)
        # 마지막 context는 "posts: post_objs"를 보여주기 위함
        # render할 땐 context로 감싸서 보내 줌
            
# write
# post - form

# 글 작성 화면
def write(request):
    if request.method == 'POST':
        # form 확인하는 작업 필요
        form = PostForm(request.POST)
        # 사용자에게 받은 POST 요청을 해당 폼에 넣어준다는 뜻 
        # 여기서 request는 사용자가 post를 작성하고 submit을 눌렀을 때 포스트를 생성
        if form.is_valid(): # 유효성 검사
            post = form.save()
            return redirect('blog:list') #urls name을 지정하면 쉽게 갈 수 있다 /blog:list
        
    # Get일 때 새롭게 form을 생성
    form = PostForm()
    return render(request,'blog/write.html',{'form': form})

# Django 자체의 클래스 뷰 기능도 강력, 편리
# model, template_name, context_object_name,
# paginate_by(페이지를 어떻게 끊어낼 것인지), form_class, form_valid() (폼확인), get_queryset()
# from django.views.generic import ListView
class List(ListView):
    model = Post # 모델 설정 models.py에서 데이터베이스 함수
    template_name = 'blog/post_list.html' # 템플릿 설정
    context_object_name = 'posts' # 템플릿(html)안의 변수 값의 이름

# Write 클래스는 form.py에 있는 것을 그냥 출력
class Write(CreateView):
    model = Post # 모델 설정
    form_class = PostForm # 폼 정함
    success_url = reverse_lazy('blog:list')
    # 성공 시 보내 줄 url
    # reverse_lazy는 url 태그를 편하게 쓰려는 함수 별칭으로 보내줄 수 있다.
    # reverse_lazy()는 클래스 / reverse()는 함수에서 사용
    # 템플릿이 지정되어 있지 않아도 PostForm이라는 것을 찾아가기 때문에 post_form.html 로 이동하게 된다. 
    

class Detail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    # 템플릿 안에 있는 변수명 
    # context_object_nams = context{posts: post_objs}와 같은 이유
    # context{:posts}를 post로 넘겨주겠다
    

class Update(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']
    # fields -> title이랑 content를 수정할 수 있게함
    # success_url = reverse_lazy('blog:list')
    # initial 기능 -> 업데이트할 때 초기의 값을 설정할 수 있게 해주는 기능 // 왜 사용? form에 값을 미리 넣어주기 위해서
    def get_initial(self):
        # initial은 form안에 포함
        initial = super().get_initial()
        # UpdateView(generic view)에서 제공하는 initial(딕셔너리)
        # get_initial은 부모에게 받은 Update에서 제공하는 기능이구나~
        post = self.get_object()
        # pk 기반으로 객체를 가져옴 원하는 하나의 값(글)을 가지고옴 
        # '수정'을 누르면 수정 화면에 뜨는 객체를 가지고 오는 것 경로에 pk로 그 값이 가지는 11,13,14 등 숫자로 객체를 가져오는 것
        
        # initial은 딕셔너리 형태로 되어 있어서 딕셔너리로 넣어야 한다.
        # post -> 현재 객체 pk -> 현재 객체 pk 타이틀과 내용을 initial에 넣어준다
        initial['title'] = post.title
        initial['content'] = post.content
        # initial['title'], initial['content'], initial[writer] 등 값을 넣어줘야지만 post_edit에서 초기화값을 줄 수 있다.
        return initial
    
    def get_success_url(self): # get_absolute_url
        post = self.get_object() # pk 기반으로 현재 객체 가져오기
        return reverse('blog:detail', kwargs={'pk': post.pk})
    # 블로그 디테일로 가져오는데 post.pk 페이지로 가져오겠다
    # http://127.0.0.1:8000/blog/detail/13/edit/ 수정화면에서 -> 수정을 하고 -> submit 버튼을 누르면
    # http://127.0.0.1:8000/blog/detail/13/ '13'으로 pk기반으로 현재 객체 가져오기 
    # post.pk는 detail 메인 페이지의 현재 객체 '13'을 가져오는 것 
    
    
class Delete(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:list')
    

class DetailView(View):
    def get(self, request, pk): # post_id: 데이터베이스 post_id 테이블 이름 사용하고 싶어서 
        # list -> object 상세 페이지 -> 상세 페이지 하나의 내용
        # pk 값을 왔다갔다, 하나의 인자
        
        # 데이터베이스 방문
        # 해당 글
        # 장고 ORM (pk: 무조건 pk로 작성해야한다.)
        post = Post.objects.get(pk=pk)
        # comment불러올 때 어떻게 불러올지 post관련된 댓글만 불러오기 때문에 저 코드를 사용한 것 
        # 댓글
        comments = Comment.objects.filter(post=post)
            # 위의 Post를 연결하는 관계 데이터베이스 on_delete를 하면 Post에서 model이 사라지면 comment에서도 사라진다 Post:Comment --> '1:N의 관계'표현 
        hashtags = HashTag.objects.filter(post=post)
        # post에 해당하는 해시태그를 models.py에서 불러옴 
        
        # 댓글 Form
        comment_form = CommentForm()
        # 폼을 렌더링해서 보여줌
        
        # 태그 Form
        hashtag_form = HashTagForm()
        
        context = {
            'post': post,
            'comments' : comments,
            'hashtags' : hashtags,
            # 'comments' : None -> 댓글이 없습니다.
            'comment_form' : comment_form,
            'hashtag_form' : hashtag_form
        }
        
        return render(request, 'blog/post_detail.html', context)
    # 렌더링이 되어야 작성할 수 있기 때문에 commentwrite, hashtagwrite 하기전에 detailview에서 렌더링 해주는 것 


### Comment
class CommentWrite(View):
    # comment는 post_detail에 보여줄거기 때문에 get은 없애도됨
    # def get(self, request):
    #     pass
    def post(self, request, pk):
        form = CommentForm(request.POST)
        # 사용자에게 받은 post요청을 form에 넣음 
        if form.is_valid():
            # form에 있는 특정 값을 가져오고 싶을 때 cleaned_data 사용하면된다.
            # 사용자에게 댓글 내용을 받아옴
            content = form.cleaned_data['content']
            # post는 post의 id값 
            # 해당 아이디에 해당하는 글 불러옴
            # request.POST에 불러온 것이 ['content']
            post = Post.objects.get(pk=pk)
            # 원래는 pk=post_id
            # Post에서 get(조건) 값 조회 post_id 불러옴
            # 댓글 객체 생성하기 위해서
            comment = Comment.objects.create(post=post, content=content)
            # models.py에서 외래키로 Post와 Comment를 연결했기 때문에 post = post(Post), content = content 실행
            # comment = Comment(post=post) -> comment.save() 을 해줘야한다
            return redirect('blog:detail', pk=pk)
        # redirect는 'get' render와 달리 url로 이동만 한다.
        # render(request, .html, context)
        

class CommentDelete(View):
    def post(self, request, pk):
        # 원래 이 pk -> comment_id
        # 지울 객체를 찾아야 한다. -> comment
        comment = Comment.objects.get(pk=pk)
        # 상세페이지로 돌아가기
        post_id = comment.post.id
        # models.py -> comment안에 있는 post 객체 id 값을 post_id에 받아준다.
        # 삭제
        comment.delete()
        
        return redirect('blog:detail', pk=post_id)
    
    
### Tag
class HashTagWrite(View):
    def post(self, request, pk):
        form = HashTagForm(request.POST)
        if form.is_valid():
            #사용자에게 태그 내용을 받아옴
            name = form.cleaned_data['name']
        # 해당 아이디에 해당 글을 부러옴 
            post = Post.objects.get(pk=pk)
        # post의 pk(id)값
        # 처음 가져 올 객체
        hashtag = HashTag.objects.create(post=post, name=name)
        # comment = Comment(post=post) -> comment.save()
        return redirect('blog:detail', pk=pk)
    

class HashTagDelete(View):
    def post(self, request, pk):
        # 해시태그의 pk(id)
        # 해시태그 불러오기
        hashtag = HashTag.objects.get(pk=pk)
        # 단수로 적어야함 1개니까 
        # 포스트 pk(id) 값 가져오기
        post_id = hashtag.post_id
        # 해시태그 삭제
        hashtag.delete()
        # 응답
        return redirect('blog:detail', pk=post_id)
        