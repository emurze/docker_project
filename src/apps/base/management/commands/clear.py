import logging

from django.core.management import BaseCommand
from taggit.models import Tag

from apps.base.models import Post, Comment

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This command fills the database'

    def handle(self, *_, **__) -> None:
        self._clear()

    @staticmethod
    def _clear() -> None:
        Post.objects.all().delete()
        Comment.objects.all().delete()
        Tag.objects.all().delete()

        logger.debug('Database has been cleaned.')
