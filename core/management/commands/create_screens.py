from django.core.management.base import BaseCommand
from core.models import Screen

class Command(BaseCommand):
    help = 'Cria as permissões padrão (telas) do sistema'

    def handle(self, *args, **kwargs):
        permissions = ['Usuários', 'Grupos']
        for name in permissions:
            screen, created = Screen.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Permissão "{name}" criada.'))
            else:
                self.stdout.write(self.style.WARNING(f'Permissão "{name}" já existe.'))
