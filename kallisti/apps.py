from django.apps import AppConfig
import logging


class KallistiConfig(AppConfig):
    name = 'kallisti'
    logger = logging.getLogger(__name__)
