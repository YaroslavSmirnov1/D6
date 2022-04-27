from django.apps import AppConfig




class NewappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newapp'

    def ready(self):
        import newapp.signals
        from .tasks import weekly_digest
        from newapp.management.commands.runapscheduler import my_job