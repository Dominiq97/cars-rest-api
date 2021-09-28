import time

from django.db import connections# type: ignore
from django.db.utils import OperationalError# type: ignore
from django.core.management.base import BaseCommand# type: ignore


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))