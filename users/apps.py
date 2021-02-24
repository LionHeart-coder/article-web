from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.db.models.signals import post_save
        from users.signals.handlers import create_registration_email

        reserved_model = self.get_model('User')
        post_save.connect(create_registration_email, sender=reserved_model, dispatch_uid="my_unique_identifier")
