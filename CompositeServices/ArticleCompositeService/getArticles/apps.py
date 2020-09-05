from django.apps import AppConfig


class GetarticlesConfig(AppConfig):
    name = 'getArticles'

    def ready(self):
        from pullFromBloombergAPI import updater
        updater.start()