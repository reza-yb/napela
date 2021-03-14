from django.core.management.base import BaseCommand
from BookAdvertisement.models import BookAd


class Command(BaseCommand):
    args = '[count]'

    def handle(self, count=20, *args, **options):

        for i in range(int(count)):
            # you can pass params explicitly
            book = BookAd(title="adams", author="khode adams", description="emza shdoe tavasote adams", sell=False)
            book.save()
