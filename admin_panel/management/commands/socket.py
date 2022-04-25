from django.core.management.base import BaseCommand
from admin_socket import Socket


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Socket')
        Socket()