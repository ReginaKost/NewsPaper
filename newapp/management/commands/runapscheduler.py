import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)



def my_job():

    for category in Category.objects.all():
        posts = Post.objects.filter(time__gt=date.today()-timedelta(weeks=1), postCategory__categories=category)
        for user in Category.objects.get(id=category.pk).subscribers.all():

            html_content = render_to_string(
                'post_dispatch_weekly.html',
                {
                    'post': posts,
                    'date': date.today()-timedelta(weeks=1),
                    'user_name': user.username,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'News and erticles in  {category} from {date.today()-timedelta(weeks=1)}',
                from_email='rksendler@gmail.com',
                to=[str(user.email)]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")


        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")