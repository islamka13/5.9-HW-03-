from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

   # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        from .signals import send_notifications, notify_about_new_post
