from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Post, Comment, HashTag
from .forms import PostForm, CommentForm, HashTagForm

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
        # MyModel.objects.all() select * from post
        context = {
            "posts": post_objs,
            'title': "Blog"
        }
        # print(post_objs) -> 콘솔에서 확인용 Queryset<[post 1,2,3,4,5]> -> 리스트 객체이기 때문에 순회 가능
        return render(request, 'blog/post_list.html', context)
        # 마지막 context는 "posts: post_objs"를 보여주기 위함
        # render할 땐 context로 감싸서 보내 줌
            

''' 
로그인 한 사람의 글을 가져오는 것? list를 표현해줄 수 있다.
class Index(LoginRequiredMixin,View):
    def get(self,request):
    # post - User 연결(Foreignkey)
    # User를 이용해서 Post를 가지고 온다.
    posts = Post.objects.filter(writer=request.user)
    context = {
        'posts':posts
    }
    return render(request, 'blog/post_list.html',context)
'''

# *write*
# post - form
# 글 작성 화면
# def write(request):
#     if request.method == 'POST':
#         # form 확인하는 작업 필요
#         form = PostForm(request.POST)
#         # request.POST는 화면에서 사용자가 입력한 내용들이 담겨있다. 사용자에게 받은 POST 요청을 해당 폼에 넣어준다는 뜻 
#         # request.POST에 담긴 title, content 값이 PostForm의 title,content 속성에 자동으로 저장되어 객체가 생성
#         if form.is_valid(): # 폼이 유효하다면
#             post = form.save()
#             # 임시저장하여 post객체를 리턴 받는다.
#             # 그래서 post_list.html에 post list에 보이게 하는 변수 post {% for post in posts %}!
#             return redirect('blog:list') #urls name을 지정하면 쉽게 갈 수 있다 /blog:list
        
    # '글작성'버튼을 누르면 생기는 form
    # 단지 '글작성'버튼은 get! get일때 생기는 form
    # form = PostForm()
    # # '글작성' 버튼 들어가면 보이는 form
    # # 하지만 이 form은 submit버튼을 눌러도 작동을 안함
    # return render(request,'blog/write.html',{'form': form})
    # form.as_p가 form:form

# Django 자체의 클래스 뷰 기능도 강력, 편리
# model, template_name, context_object_name,
# paginate_by(페이지를 어떻게 끊어낼 것인지), form_class, form_valid() (폼확인), get_queryset()
# from django.views.generic import ListView
# class List(ListView):
#     model = Post # 모델 설정 models.py에서 데이터베이스 함수
#     template_name = 'blog/post_list.html' # 템플릿 설정
#     context_object_name = 'posts' # 템플릿(html)안의 변수 값의 이름

# *class write*
# class Write(CreateView):
#     model = Post # 모델 설정
#     form_class = PostForm # 폼 정함
#     # 템플릿이 지정되어 있지 않아도 PostForm이라는 것을 찾아가기 때문에 post_form.html 로 이동하게 된다. 
#     success_url = reverse_lazy('blog:list')
    # 성공 시 보내 줄 url
    # reverse_lazy는 url 태그를 편하게 쓰려는 함수 별칭으로 보내줄 수 있다.
    # reverse_lazy()는 클래스 / reverse()는 함수에서 사용

class Write(LoginRequiredMixin,View):
    # Mixin : LoginRequiredMixin -> 로그인 된 사람만 접근할 수 있게 한다. 
    # 로그인 되지 않은 사용자는 작동되지 않는다 -> 그럴땐 redirect로 login경로로 보내줌
    # 글작성 버튼을 눌렀을 때 로그인이 안되었을시엔 로그인 하고 오라고 로그인 페이지로 설정
    # login_url = '/user/login' -> settigs.py에서 경로 지정해줌
    # redirect_field_name = 'next'
    # 키워드를 next로 해주겠다 회원가입으로 가고싶으면
    
    def get(self,request):
        # next_path = request.GET.get('next')
        # next_url = request.GET.get(self.redirect_field_name)
        
        form = PostForm()
        context = {
            'form': form,
            'title': "Blog"
        }
        return render(request,'blog/post_form.html',context)
    
    def post(self,request): # response -> HttpResponse객체
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # 저장하긴 하는데 commit=False라고 넣어주면 뒤의 내용이 바뀔수도 있다라는 의미
            # 중복 DB save를 방지
            # 작성자 정보 가져오기
            post.writer = request.user
            # post.writer 컬럼에 request.user값을 넣어주는 것 
            post.save()
            return redirect('blog:list') # response -> HttpResponse객체
        # form.add_error(None,'폼이 유효하지 않습니다.')
        # 폼이 유효하지 않으면 에러 추가
        context = {
            'form': form
        }
        return render(request,'blog/post_form.html')
    
    
# *class detail*
# class Detail(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'
#     context_object_name = 'post'
#     # 템플릿 안에 있는 변수명 
    # context_object_nams = context{posts: post_objs}와 같은 이유
    # context{:posts}를 post로 넘겨주겠다
    
    
# *class update*
# class Update(UpdateView):
#     model = Post
#     template_name = 'blog/post_edit.html'
#     fields = ['title', 'content']
#     # fields -> title이랑 content를 수정할 수 있게함
#     # success_url = reverse_lazy('blog:list')
#     # initial 기능 -> 업데이트할 때 초기의 값을 설정할 수 있게 해주는 기능 // 왜 사용? form에 값을 미리 넣어주기 위해서
#     def get_initial(self):
#         # initial은 form안에 포함
#         initial = super().get_initial()
#         # UpdateView(generic view)에서 제공하는 initial(딕셔너리)
#         # get_initial은 부모에게 받은 Update에서 제공하는 기능이구나~
#         post = self.get_object()
#         # 여기서 self는 model = Post
#         # pk 기반으로 객체를 가져옴 원하는 하나의 값(글)을 가지고옴 
#         # '수정'을 누르면 수정 화면에 뜨는 객체를 가지고 오는 것 경로에 pk로 그 값이 가지는 11,13,14 등 숫자로 객체를 가져오는 것
#         # 현재 오브젝트를 pk값을 이용해서 가져오는 것 -> 현재 pk값에 해당하는 post객체(오브젝트)자체를 가져온다는 뜻 숫자값을 이용해서 객체를 가져온다.
        
#         # initial은 딕셔너리 형태로 되어 있어서 딕셔너리로 넣어야 한다.
#         # post -> 현재 객체 pk -> 현재 객체 pk 타이틀과 내용을 initial에 넣어준다
#         initial['title'] = post.title
#         initial['content'] = post.content
#         # initial['title'], initial['content'], initial[writer] 등 값을 넣어줘야지만 post_edit에서 초기화값을 줄 수 있다.
#         return initial
    
#     def get_success_url(self): # get_absolute_url
#         post = self.get_object() # pk 기반으로 현재 객체 가져오기
#         return reverse('blog:detail', kwargs={'pk': post.pk})
    # 블로그 디테일로 가져오는데 post.pk 페이지로 가져오겠다
    # http://127.0.0.1:8000/blog/detail/13/edit/ 수정화면에서 -> 수정을 하고 -> submit 버튼을 누르면
    # http://127.0.0.1:8000/blog/detail/13/ '13'으로 pk기반으로 현재 객체 가져오기 
    # post.pk는 detail 메인 페이지의 현재 객체 '13'을 가져오는 것 
    
    
class Update(View):
    def get(self,request,pk): # post_id
        ## try, except
        try:
            post = Post.objects.get(pk=pk) # <Object : post>
        # get()은 해당 조건이 없을 때 오류를 발생시킨다.
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        form = PostForm(initial={'title':post.title,'content':post.content})
        context = {
            'form': form,
            'post': post,
            'title': "Blog"
            # post를 같이 넘겨주어야 주소를 정확히 넘겨줄 수 있었다.
        }
        return render(request, 'blog/post_edit.html',context)
    
    def post(self, request, pk):
        ## try, except
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('blog:detail', pk=pk) #post_id
        
        # form.add_error('폼이 유효하지 않습니다.')
        context = {
            'form': form,
            'title': "Blog"
        }
        return render(request, 'blog/post_edit.html', context)
    
    
# *class delete*
# class Delete(DeleteView):
#     model = Post
#     success_url = reverse_lazy('blog:list')
#     # 삭제는 post로 해줄 필요가 없으니 'get'


class Delete(View):
    def post(self, request, pk): # pk = post_id
        ## try, except
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        
        post.delete() # post.save() 저장을 할 것이 없으니까 저장 할 필요가 없다.
        return redirect('blog:list')
    
    # 클래스 자체에 아예 접근하지 못하게 -> LoginRequireMixin
    # Login이 되었을 때만 삭제 버튼이 보이게



class DetailView(View):
    def get(self, request, pk): # post_id: 데이터베이스 post_id 테이블 이름 사용하고 싶어서 
        # list -> object 상세 페이지 -> 상세 페이지 하나의 내용
        # pk 값을 왔다갔다, 하나의 인자
        
        # 데이터베이스 방문
        # 해당 글
        # 장고 ORM (pk: 무조건 pk로 작성해야한다.)
        # post = Post.objects.get(pk=pk)
        # Post.objects.all()은 내가 썼던 모든 글을 불러오는 것이기 때문에 여기에선 detail 페이지고 해당 글 하나를 선택해서 가져오기 때문에 get(pk=pk)라고 해줘야함
        # 예를들면 admin에 접속하면 Post Object(19) 이 제목이랑 내용만 가져오는 것 
        
        # 댓글
        # comments = Comment.objects.filter(post=post) 1
        # comment불러올 때 어떻게 불러올지 post관련된 댓글만 불러오기 때문에 저 코드를 사용한 것
        # 포스트 안에 있는 comment를 보여줌
        # 예를들면 admin에 들어가면 Post Object(19)의 작성된 comment를 가져오는 것 -> 그리고 comment를 쉽게 보기 위해서 'Commnet on 포스트 제목' 으로 명시해놓음
        # 위의 Post를 연결하는 관계 데이터베이스 on_delete를 하면 Post에서 model이 사라지면 comment에서도 사라진다 Post:Comment --> '1:N의 관계'표현'
        
        # 해시태그
        # hashtags = HashTag.objects.filter(post=post) 2
        # post에 해당하는 해시태그를 models.py에서 불러옴 
        
        # 댓글
        # Object.objects.select_related('참조 관계를 갖는 필드명')
        # comments = Comment.objects.select_related('post').filter(post__pk=pk) #-> comments[0]
        # hashtags = HashTag.objects.select_related('post').filter(post__pk=pk)
        # commets는 복수니까 filter을 써야 복수로 값을 가지고 온다
        # comments = Comment.objects.select_related('writer').filter(post=post)
        # comments = Comment.objects.select_related('writer').filter(post__pk=pk)
        # post가 comment를 참조할 수 있으니까 이렇게도 써도 된다
        # comment = Comment.objects.select_related('post').first()
        # post안의 pk값 숫자로도 값을 찾아 올 수 있다
        # 저 'writer'은 포린키로 연결된 것을 말하는 것 불러오는게 아님
        # 해시태그
        # hashtags = HashTag.objects.select_related('writer').filter(post=post)
        # hashtags = HashTag.objects.select_related('writer').filter(post__pk=pk)
        # print(comments)
        # <QuerySet[]>
        # value.attr
        # print(hashtags)
        
        # 글
        # Object.objects.prefetch_related('역참조필드_set').get(조건)
        post = Post.objects.prefetch_related('comment_set', 'hashtag_set').get(pk=pk)
        # post는 post 자신이니까 pk=pk라고 표기
        
        comments = post.comment_set.all()
        hashtags = post.hashtag_set.all()
        
        print(comments)
        print(hashtags)
        print(post)
        
        # 댓글 Form
        comment_form = CommentForm()
        # 폼을 렌더링해서 보여줌
        
        # 태그 Form
        hashtag_form = HashTagForm()
        
        context = {
            'title': "Blog",
            'post_id' : pk,
            # 'post_title' : post.title,
            # 'post_content': post.content,
            # 'post_writer': post.writer,
            # 'post_created_at': post.created_at,
            # 'comments' : comments,
            # 'hashtags' : hashtags,
            # 'comment_form' : comment_form,
            # 'hashtag_form' : hashtag_form,
        }
        
        return render(request, 'blog/post_detail.html', context)
    # 렌더링이 되어야 작성할 수 있기 때문에 commentwrite, hashtagwrite 하기전에 detailview에서 렌더링 해주는 것 


### Comment
class CommentWrite(LoginRequiredMixin, View):
    # comment는 post_detail에 보여줄거기 때문에 get은 없애도됨
    # def get(self, request):
    #     pass
    '''
    1. LoginRequiredMixin -> 삭제
    2. 비회원 유저 권한 User
    '''
    def post(self, request, pk):
        # 사용자에게 받은 post요청을 form에 넣음
        form = CommentForm(request.POST)
        # 해당 아이디에 해당하는 글 불러옴
        ## try, except
        try:
            post = Post.objects.get(pk=pk) # <Object: post>
        # get()은 해당 조건이 없을 때 오류를 발생시킨다. 
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        # get 관련 쿼리들은 해당 데이터가 없을 때 오류 발생
        # get_or_404
        
        if form.is_valid():
            # form에 있는 특정 값을 가져오고 싶을 때 cleaned_data 사용하면된다.
            # 사용자에게 댓글 받아옴
            content = form.cleaned_data['content']
            # request.POST에 불러온 것이 ['content']
            # 유저 정보 가져오기
            writer = request.user
            # 댓글 객체 생성(저장), create 메서드를 사용할 때는 save 필요없음
            # comment는 위의 post(post객체), content(글내용), writer(작성자)를 저장해주는 역할
            try:
                comment = Comment.objects.create(post=post, content=content, writer=writer)
            # models.py에서 외래키로 Post와 Comment를 연결했기 때문에 post = post(Post), content = content 실행
            # comment = Comment(post=post) -> comment.save() 을 해줘야한다
            # 생성 할 값이 이미 있다면 오류 발생, Unique 값이 중복될 때 오류 발생
            # 필드 값이 비어있을 때 : ValidationError
            # 외래키 관련 데이터베이스 오류 : ObjectDoseNotExist
            # 그래서 이 오류를 발생시키지 않기 위해 나온 것이
            # get_or_create() -> 2가지 경우의 리턴값
            
            # comment, created = Comment.objects.get_or_create(post=post, content=content, writer=writer)
            # 값이 있다면 comment에다 넣어주고 값이 없다면 created에 저장(생성)
            
            # if created: print('생성되었습니다') else: print('이미 있습니다')
            except ObjectDoesNotExist as e:
                print('Post does not exist.', str(e))
            
            except ValidationError as e:
                print('Validation error occurred', str(e))
            
            # 폼을 submit 하고 나서 url 이동
            return redirect('blog:detail', pk=pk)
        # redirect는 'get' render와 달리 url로 이동만 한다.
        # render(request, .html, context)
    
        # form.add_error(None,'폼이 유효하지 않습니다.')
        # errors = [error for error_list in form.errors.values() for error in error_list]
        
        hashtag_form = HashTagForm()
        # 자동으로 오류가 들어있는 폼을 출력
        context = {
            'title': "Blog",
            'post_id': pk, #pk로 찾아옴
            # post.title, post.content
            'comments': post.comment_set.all(), 
            # post와 ForeignKey라 역참조로 가지고 옴
            'hashtags': post.hashtag_set.all(),
            'comment_form': form,
            'hashtag_form': hashtag_form
        }
        return render(request,'blog/post_detail.html', context)
    ## 에러폼 
    #1. post_detail.html 자체에 태그 조건을 걸어준다.
    #2. 예외 처리 용 파일을 만들어서 post_detail.html 안에 포함시켜준다.


class CommentDelete(View):
    def post(self, request, pk): # comment_id
        # 지울 객체를 찾아야 한다. -> 댓글 객체(comment)
        ## try, except
        try:
            comment = Comment.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Comment does not exist', str(e))
        # post요청시 {% url 'blog:cm-delete' pk=comment.pk %} url에 정해준 값이 comment의 pk값이고, 위에 코드는 해당 pk값을 가지고 있는 comment를 디비에서 불러오는 과정
        # commet의 지울 객체를 찾아야 해서 사용한 코드
        # 해당 pk값을 가지고 있는 comment를 데이터베이스에서 불러오는 것
        post_id = comment.post.id
        # 삭제 완료 후, post_detail 페이지로 돌아가기 위해서는 post 객체 자체의 pk(id) 값을 알아야함 그래서 comment 안에 foreignkey로 연결된 post에 접근(.)해서 그 post의 id 값을 가져와야 하는 것. 이렇게 해야 댓글 삭제 뒤, 그 댓글이 달려있던 상세 페이지로 이동할 수 있기 때문
        # models.py -> comment안에 있는 post 객체 id 값을 post_id에 받아준다.
        # 삭제
        comment.delete()
        
        # 상세페이지로 돌아가기
        return redirect('blog:detail', pk=post_id)
    
    
### Tag
class HashTagWrite(LoginRequiredMixin, View):
    def post(self, request, pk): # post_id
        form = HashTagForm(request.POST)
        # 해당 아이디에 해당 글을 불러옴
        ## try, except
        try:
            comment = Comment.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Comment does not exist.', str(e))
        
        if form.is_valid(): 
            #사용자에게 태그 내용을 받아옴
            name = form.cleaned_data['name']
            # 작성자 정보 가져오기
            writer = request.user
            
            # 해시태그 객체 생성(저장), create 메서드를 사용할 때는 save 필요 없음
            # 해시태그 객체를 저장하기 위한 함수
            try:
                hashtag = HashTag.objects.create(post=post, name=name, writer=writer)
                
            # comment = Comment(post=post) -> comment.save()
            except ObjectDoesNotExist as e:
                print('Post does not exist.', str(e))
                
            except ValidationError as e:
                print('Validation error occurred', str(e))
            
            return redirect('blog:detail', pk=pk)
        
        # form.add_error(None,'폼이 유효하지 않습니다.')
        comment_form = CommentForm()
        
        context = {
            'title': "Blog",
            'post': post,
            'comments': post.comment_set.all(),
            'hashtags':post.hashtag_set.all(),
            'comment_form': comment_form,
            'hashtag_form': form
        }
        return render(request,'blog/post_detail.html',context)


class HashTagDelete(View):
    def post(self, request, pk): # hashtag_id
        # 해시태그 불러오기
        # 지울 객체를 찾아야 한다. -> 태그 객체
        try:
            hashtag = HashTag.objects.get(pk=pk)
            # 단수로 적어야함 1개니까 
            
        except ObjectDoesNotExist as e:
            print('HashTag does not exist.',str(e))
        
        # 상세 페이지로 돌아가기
        post_id = hashtag.post.id
        # 포스트 pk(id) 값 가져오기
        # 삭제
        hashtag.delete()
        # 응답
    
        return redirect('blog:detail', pk=post_id)
        