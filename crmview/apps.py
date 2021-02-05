from django.apps import AppConfig


class CrmviewConfig(AppConfig):
    name = 'crmview'

    def ready(self):
        import crmview.signals