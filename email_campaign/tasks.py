from django.core.mail import send_mail
from django.utils import timezone
from smtplib import SMTPException

from config import settings
from config.celery import app
from celery import Task

from email_campaign.models import MailingCampaign, Log


class MailingTask(Task):
    autoretry_for = (SMTPException,)
    max_retries = 3
    ignore_result = True


def send_mails() -> None:
    """Send email to clients"""
    now = timezone.now()
    ready_to_mail_list = MailingCampaign.objects.filter(next_time_run__le=now)

    for mailing in ready_to_mail_list:
        _send_one_message.delay(mailing.pk)


@app.task(base=MailingTask)
def _send_one_message(mailing_pk: int) -> None:
    mailing: MailingCampaign = MailingCampaign.objects.get(pk=mailing_pk)
    recipient_email: list[str] = [client.email for client in mailing.mail_clients.all()]

    try:
        if recipient_email:
            send_mail(
                mailing.mail_subject,
                mailing.body,
                settings.EMAIL_HOST_USER,
                recipient_email,
                fail_silently=False,
            )
            logs = []
            for client in mailing.mail_clients.all():

                log = Log(
                    log_status=Log.STATUS_SUCCESSFUL,
                    log_client=client,
                    log_mailing=mailing,
                    log_server_response='Email Sent Successfully!',
                )
                logs.append(log)
            Log.objects.bulk_create(logs)

    except SMTPException as err:
        logs =[]
        for client in mailing.mail_clients.all():
            log = Log(
                log_status=Log.STATUS_FAILED,
                log_client=client,
                log_mailing=mailing,
                log_server_response=err,
            )
            logs.append(log)
        Log.objects.bulk_create(logs)

        raise
