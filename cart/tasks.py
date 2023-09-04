from __future__ import absolute_import, unicode_literals

from celery import shared_task
from config.celery import app



@shared_task
def add(x, y):
    print('\n"-_-"' * 20, x+y, '\n"-_-"' * 20)
    return

def add_(x, y):
    print('\n"-_-"' * 20, x+y, '\n"-_-"' * 20)
    return


