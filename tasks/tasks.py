from asyncio import tasks
from unicodedata import name
from django_q.tasks import schedule
from django_q.models import Schedule

def add1(x, y):
    return x + y

Schedule.objects.create(name='add1' ,func='tasks.tasks.add1',
        args='3, 4',
        schedule_type=Schedule.CRON,
        cron = '0 22 * * 1-5')
Schedule.save()