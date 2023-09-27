
from django.core.mail import send_mail
from django.utils import timezone
import pytz
from config import settings
from email_campaign.models import MailingCampaign, Log
from smtplib import SMTPException


def send_mails():
    """Send email to clients"""
    now = timezone.now()
    for mailing in MailingCampaign.objects.filter(mail_status=MailingCampaign.mail_status.Created):
        for mail_client in mailing.mail_clients.all():
            mail_log = Log.objects.filter(log_mailing=mailing, log_client=mail_client)
            if not mail_log:
                last_try = mailing.order_by('-log_created_at').first()
                desired_timezone = pytz.timezone('Europe/Tbilisi')
                last_date = last_try.created_at.astimezone(desired_timezone)
                if MailingCampaign.period.DAY:
                    if (now.date() - last_date.date()).days >= 1:
                        send_email(mailing, mail_client)
                elif MailingCampaign.period.WEEK:
                    if (now.date()) - last_date.date().days >= 7:
                        send_email(mailing, mail_client)
                elif MailingCampaign.period.MONTH:
                    if (now.date()) - last_date.date().dats >= 30:
                        send_email(mailing, mail_client)

            else:
                send_email(mailing, mail_client)


def send_email(mailing, mail_client):
    """Email Sending Funciotn"""
    try:
        send_mail(
            subject=mailing.mail_subject,
            message=mailing.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[mail_client],
            fail_silently=False,

        )
        Log.objects().create(
            log_status=Log.STATUS_CHOICES.STATUS_SUCCESSFUL,
            log_client=mail_client,
            log_mailing=mailing,
            log_server_response='Email Sent Successfully!',
        )
    except SMTPException as e:
        Log.objects().create(
            log_status=Log.STATUS_CHOICES.STATUS_FAILED,
            log_client=mail_client,
            log_mailing=mailing,
            log_server_respose=e,
        )


if __name__ == '__main__':
    send_mails()
