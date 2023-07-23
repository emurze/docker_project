from django.core.management import BaseCommand

from src.apps.base.models import Post
from src.utils.query_debugger import query_debugger


class Command(BaseCommand):
    help = 'This command fills the database'

    def handle(self, *_, **__) -> None:
        self.test()

    @query_debugger
    def test(self) -> None:
        post = Post.objects.prefetch_related('comments')
        print(post)
