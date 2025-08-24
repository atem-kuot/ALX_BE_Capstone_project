from django.apps import AppConfig


class MedicinesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medicines'
    
    def ready(self):
        import medicines.signals