import logging

from django.db.models import Subquery
from django.http import Http404
from django.views.generic import ListView
from taggit.models import Tag

from apps.base.models import Post

logger = logging.getLogger(__name__)


class PostList(ListView):
    template_name = 'pages/list/list.html'
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        print('PRINT LIST')
        logger.debug('DEBUG LIST')
        logger.info('INFO LIST')
        logger.warning('WARNING LIST')
        logger.error('ERROR LIST')
        logger.critical('CRITICAL LIST')

        if tag_slug := self.kwargs.get('tag_slug'):
            tag = Tag.objects.filter(slug=tag_slug)
            posts = Post.objects.filter(tags=Subquery(tag.values('pk')[:1]))

            self.kwargs['tag'] = tag.get()

            if not posts.exists():
                raise Http404()
        else:
            posts = Post.objects.all()

        return posts

    def get_context_data(self, *args, **kwargs):
        kwargs['tag'] = self.kwargs.get('tag')
        return super().get_context_data(*args, **kwargs)
