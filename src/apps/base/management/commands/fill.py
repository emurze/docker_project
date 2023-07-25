import logging
import random
from operator import attrgetter

import lorem
from django.core.management import BaseCommand
from taggit.models import Tag

from apps.base.models import Post, Comment

DEFAULT_COUNT = 100
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This command fills the database'

    @staticmethod
    def _fill(count: int = DEFAULT_COUNT) -> None:
        Post.objects.all().delete()
        Comment.objects.all().delete()
        Tag.objects.all().delete()

        tags = [
            Tag(
                name=f'tag_{index}',
                slug=f'tag-{index}',
            )
            for index in range(1, count // (DEFAULT_COUNT // 10))
        ]
        Tag.objects.bulk_create(tags)

        posts = [
            Post(
                pk=index,
                title=f'post {index}',
                slug=f'post-{index}',
                content=lorem.paragraph(),
                author_id=1,
            )
            for index in range(1, count+1)
        ]

        comments = []
        for index, post in enumerate(posts):
            logger.debug(f'post {index}')
            random_tags = random.sample(tags, 5)
            post.tags.add(*map(attrgetter('name'), random_tags))
            comments += (
                Comment(post=post, user_id=1, content=content)
                for content in range(1, 6)
            )

        Post.objects.bulk_create(posts)
        Comment.objects.bulk_create(comments)

    def add_arguments(self, parser) -> None:
        parser.add_argument("-c", nargs="+", type=int)

    def handle(self, *_, **options) -> None:
        if c := options.get('c'):
            self._fill(c[0])
        else:
            self._fill()
