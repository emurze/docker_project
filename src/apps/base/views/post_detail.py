from functools import lru_cache

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from apps.base.forms import CommentForm
from apps.base.models import Post


class PostDetail(DetailView):
    model = Post
    template_name = 'pages/detail/detail.html'
    context_object_name = 'post'
    object = None

    def post(self, request, **kwargs):
        self.object = self.get_object()

        if (comment_form := CommentForm(request.POST)).is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = self.object

            if parent_id := request.POST.get('parent_id'):
                comment.parent_id = parent_id

            comment.save()
            comment_form = CommentForm()

        context = self.get_context_data(object=self.object)
        context['comment_form'] = comment_form
        return self.render_to_response(context)

    @lru_cache
    def get_object(self, queryset=None) -> Post:
        if queryset is None:
            queryset = self.get_queryset()
        kwargs = self.kwargs
        post = get_object_or_404(
            queryset,
            slug=kwargs.get('slug'),
            publish__year=kwargs.get('year'),
            publish__month=kwargs.get('month'),
            publish__day=kwargs.get('day'),
        )
        return post

    def get_context_data(self, **kwargs):
        post = kwargs['object']
        comments = post.comments.exclude(parent__isnull=False)
        kwargs |= {
            # On <GET>, <POST> success -> clear form,
            # On <POST> error -> form with data.
            'comment_form': kwargs.get('comment_form', CommentForm()),
            'comments': comments
        }
        return super().get_context_data(**kwargs)
