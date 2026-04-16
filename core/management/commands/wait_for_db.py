"""
Django command to wait for db to be available.
"""
import time
from django.core.management import BaseCommand
from psycopg2.errors import OperationalError as psycopg2Error
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Django command to wait for db to be available."""
    def handle(self, *args, **options):
        self.stdout.write('waiting for db...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (OperationalError, psycopg2Error):
                self.stdout.write(self.style.ERROR('Database unavailable waiting 1 second.'))
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available.'))
