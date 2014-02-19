from django.core.management.base import BaseCommand, CommandError

from notifier.models import Pruefungsplan


class Command(BaseCommand):
    help = 'Updates the pruefungsplans and sends out notifications'

    def handle(self, *args, **options):
        for pruefungsplan in Pruefungsplan.objects.filter(is_available=False):
            self.stdout.write('Updating %s...' % pruefungsplan.name)
            pruefungsplan.update()
