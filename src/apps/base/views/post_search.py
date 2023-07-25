import logging

from django.contrib.postgres.search import SearchVector, SearchQuery, \
    SearchRank
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.base.forms import SearchForm
from apps.base.models import Post

logger = logging.getLogger(__name__)


class PostSearch(View):
    template_name = 'pages/search/search.html'

    def get(self, request: WSGIRequest) -> HttpResponse:
        logger.debug("Attempting to search")

        context = {}
        form = SearchForm(request.GET)

        if request.GET.get('query') and form.is_valid():
            cleaned_query = form.cleaned_data['query']
            query = SearchQuery(cleaned_query)
            vector = SearchVector('content')
            posts = Post.published.annotate(rank=SearchRank(vector, query))\
                                  .order_by('-rank')[:10]
            context |= {
                'posts': posts,
            }
            logger.debug(f'search found {posts.count()} posts')

        context |= {'form': SearchForm()}
        return render(request, self.template_name, context)
