from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, RedirectView
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from comments.forms import CommentForm
from comments.models import Comment
from .models import Post
from .forms import PostForm


# def anon_permissions(item, user):
#     if not user.is_authenticated


class NewsList(View):
    '''
    Returns news list for any user
    '''

    def get(self, request):
        search = request.GET.get('search')
        posts_list = Post.objects.active()  # Custom model manager see models.py
        if search:
            posts_list = posts_list.filter(
                Q(title__icontains=search) |
                Q(context__icontains=search) |
                Q(author__first_name__icontains=search)
            ).distinct()
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, "post_list.html", {"posts": posts})


class NewsCreate(View):
    '''
    Returns post creation form and handle post creation
    '''
    @method_decorator(login_required)
    def get(self, request):
        if request.user.is_authenticated:
            form = PostForm()
            return render(request, "post_create.html", {"form": form})


    def post(self, request):
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post sended to draft")
            return redirect(post.get_absolute_url())
        return render(request, "post_create.html", {"form": form})


class NewsDetail(View):
    '''
    Return specific details about selected post with comments
    '''

    def get(self, request, slug=None):
        post = get_object_or_404(Post, slug=slug)
        if (post.deleted):
            raise Http404
        if (post.draft == False and request.user != post.author):
            raise Http404
        initial = {
            "content_type": post.get_content_type,
            "object_id": post.id
        }
        comment_form = CommentForm(request.POST or None, initial=initial)
        comments = post.comments
        post.view_counter()
        return render(request, "post_detail.html", {"detail": post,
                                                    "comments": comments,
                                                    "form": comment_form})

    def post(self, request, slug=None):
        print(request.body)
        print(request.POST)
        post = get_object_or_404(Post, slug=slug)
        initial = {
            "content_type": post.get_content_type,
            "object_id": post.id
        }
        comment_form = CommentForm(request.POST or None, initial=initial)
        if comment_form.is_valid():
            c_type = comment_form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=c_type)
            obj_id = comment_form.cleaned_data.get("object_id")
            content_data = comment_form.cleaned_data.get("content")
            parent_obj = None
            try:
                parent_id = request.POST.get("parent_id")
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(user=request.user,
                                                                 content_type=content_type,
                                                                 object_id=obj_id,
                                                                 content=content_data,
                                                                 parent=parent_obj)
        return redirect(post.get_absolute_url())

class CommentDelete(View):
    '''
    Handle post comment delete
    '''
    #TODO
    #change method to post

    def get(self, request, slug, id=None):
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(Comment, id=id)
        if request.user == comment.user or request.user.is_staff:
            comment.set_deleted()
            return redirect(post.get_absolute_url())
        response = HttpResponse("You cant delete other user comment")
        response.status_code = 403
        return response

class NewsUpdate(View):
    '''
    Handle editing chosen post
    '''

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.user != post.author:
            raise Http404
        form = PostForm(instance=post)
        context = {
            "post": post,
            "form": form
        }
        return render(request, "post_edit.html", context)

    def post(self, request, slug):
        if not request.user.is_authenticated:
            raise Http404
        post = get_object_or_404(Post, slug=slug)
        if request.user != post.author:
            raise Http404

        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated = timezone.now()
            post.save()
            messages.success(request, "Succesfully Updated!")
            return redirect(post.get_absolute_url())
        return render(request, "post_edit.html", {"form": form})


class NewsDelete(View):
    '''
    Handle deleting chosen post
    '''

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        messages.success(request, "Successfully deleted!")
        post.set_deleted()
        return redirect("news:post_list")


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs.get("id")
        post = get_object_or_404(Post, id=id)
        url_ = post.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
        return url_
