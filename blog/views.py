from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
# Create your views here.

from .models import Post
from .forms import PostForm, UserForm

# TODO add logging (sentry on dev project)

@method_decorator(login_required, name='dispatch')
class CreateNewPostView(CreateView):
    """ Create a new POst object """

    model = Post
    form_class = PostForm
    template_name = 'create_new_post.html'
    success_url = reverse_lazy('posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'author': self.request.user})
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ShowListPostsView(ListView):
    """ Show list of posts from all users"""

    form_class = PostForm
    template_name = 'posts.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_publish=True)


class ShowPostDetailView(DetailView):
    """ Show post detail """
    model = Post
    form_class = PostForm
    template_name = 'post_detail.html'


@method_decorator(login_required, name='dispatch')
class ChangePostView(UpdateView):
    """ change post text or title """
    model = Post
    form_class = PostForm
    template_name = 'change_post.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        if self.request.user.id == form.instance.author_id:
            return super().form_valid(form)
        return HttpResponseForbidden()


@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    """ Delete post not added to urls """
    model = Post
    form_class = PostForm
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('posts')


@method_decorator(login_required, name='dispatch')
class ShowUsersListView(ListView):
    """ Show list of all user  """
    queryset = get_user_model().objects.all()
    form_class = UserForm
    template_name = 'users.html'
    paginate_by = 1


@method_decorator(login_required, name='dispatch')
class ShowUserDetailView(DetailView):
    """ Not use for now """
    model = get_user_model()
    form_class = UserForm
    template_name = 'users.html'


@method_decorator(login_required, name='dispatch')
class ShowCertainUserPosts(ListView):
    """ Show all post from certain user """
    form_class = PostForm
    template_name = 'posts.html'
    paginate_by = 1

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Post.objects.filter(author_id=pk, is_publish=True)


class CustomLoginView(LoginView):
    """ Login view  """
    template_name = 'admin/login.html'