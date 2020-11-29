from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.models import Profile
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import (
    CreateView,
    # DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from .models import Comment, Post
from .forms import CommentForm


def home(request):
    return render(request, "blog/home.html")


class PostListView(ListView):
    model = Post
    template_name = "blog/blog.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


# class PostDetailView(DetailView):
#     model = Post


def post_detail(request, pk):
    """detail"""
    post = get_object_or_404(Post, id=pk)
    author_profile = get_object_or_404(Profile, user=request.user.id)
    avatar = author_profile.image.url
    comments = post.comments.all()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    comment_form = CommentForm()

    context = {
        "object": post,
        "comments": comments,
        "form": comment_form,
        "new_comment": new_comment,
        "avatar": avatar,
    }

    return render(request, "blog/post_detail.html", context)


# def add_comment_to_post(request, pk):
#     """add comment"""

#     post = get_object_or_404(Post, id=pk)
#     current_profile = get_object_or_404(Profile, user=request.user.id)
#     avatar = current_profile.image.url
#     comments = post.comments.all()
#     new_comment = None
#     if request.method == "POST":
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.user = request.user
#             new_comment.save()
#             return redirect('post-detail', pk=post.pk)

#     return render(request, "blog/home.html")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image"]
    success_url = "/blog/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/blog/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    """About"""

    return render(request, "blog/about.html")
