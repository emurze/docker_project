from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


DEFAULT_ADMIN_NAME = 'adm1'
DEFAULT_ADMIN_EMAIL = 'adm1@adm1.com'
DEFAULT_ADMIN_PASSWORD = 'adm1'

User = get_user_model()


class Command(BaseCommand):
    help = 'This command create superuser'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser) -> None:
        parser.add_argument("--username")
        parser.add_argument("--email")
        parser.add_argument("--password")

    def handle(self, *_, **options) -> None:
        if not User.objects.exists():
            user = User.objects.create_superuser(
                username=options.get('username', DEFAULT_ADMIN_NAME),
                email=options.get('email', DEFAULT_ADMIN_EMAIL),
                password=options.get('password', DEFAULT_ADMIN_PASSWORD)
            )
            print(f'{user.username} was created.')
