from django.apps import AppConfig


class UserportalConfig(AppConfig):
    name = 'userPortal'
    verbose_name = "Child Users"
    
    def ready(self):
        import userPortal.signals.handlers
