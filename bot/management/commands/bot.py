from django.core.management.base import BaseCommand
from tg_bot import Bot
import os 

class Command(BaseCommand):
    


    def handle(self, *args, **kwargs):
        # os.chdir("media/")
        Bot()