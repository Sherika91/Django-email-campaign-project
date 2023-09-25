import datetime
from time import timezone

from django.db import models
from config import settings

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """Client model"""
    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Client owner',
                                     **NULLABLE, )
    email = models.EmailField(max_length=150, unique=True, **NULLABLE, verbose_name='Email', )
    first_name = models.CharField(max_length=100, verbose_name='First Name', **NULLABLE, )
    last_name = models.CharField(max_length=100, verbose_name='Last Name', **NULLABLE, )
    comment = models.TextField(**NULLABLE, verbose_name='Comment', )

    def __str__(self):
        return f"{self.email} ({self.first_name} {self.last_name})"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class MailingPeriod(models.IntegerChoices):
    DAY = 1, 'daily'
    WEEK = 2, 'weekly'
    MONTH = 3, 'Mmnthly'

    def __str__(self) -> str:
        return self.label


class MailingStatus(models.IntegerChoices):
    FINISHED = 1, 'finished'
    CREATED = 2, 'created'
    RUNS = 3, 'runs'

    def __str__(self) -> str:
        return self.label


class MailingCampaign(models.Model):
    """Campaign model"""
    send_time = models.TimeField(verbose_name='Send time', **NULLABLE, )
    period = models.SmallIntegerField(choices=MailingPeriod.choices, verbose_name='Frequency', **NULLABLE, )
    mail_status = models.SmallIntegerField(choices=MailingStatus.choices, verbose_name='Status',
                                           default=MailingStatus.CREATED)
    next_time_run = models.DateTimeField(verbose_name='Next time run', null=True, )
    mail_clients = models.ManyToManyField(Client, verbose_name='Clients', **NULLABLE, )
    mail_subject = models.CharField(max_length=100, verbose_name='Subject', **NULLABLE, )
    body = models.TextField(verbose_name='Body', **NULLABLE)
    mail_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Campaign owner',
                                   **NULLABLE, )

    def __str__(self):
        return f"{self.mail_subject} в {self.send_time} ({self.period}"

    def get_next_time_run(self) -> datetime:
        """Return next time run"""
        now = timezone.now()
        if self.send_time >= now.time():
            # if time of start is 10:00 and now is 09:00
            # we will send email today
            next_datetime = now.today()
        else:
            match self.period:
                case MailingPeriod.DAY:
                    next_datetime = now.today() + datetime.timedelta(days=1)
                case MailingPeriod.WEEK:
                    next_datetime = now.today() + datetime.timedelta(days=7)
                case MailingPeriod.MONTH:
                    next_datetime = now.today() + datetime.timedelta(days=30)
                case _:
                    raise ValueError('Unknown period')

        return datetime.combine(next_datetime.date(), self.send_time)

    def save(self, *args, **kwargs):
        if self.pk:  # Если объект уже в базе
            cls = self.__class__
            old_object = cls.objects.select_for_update().get(pk=self.pk)
            if old_object.time == self.send_time and old_object.period == self.period:
                # if time and period not changed we are not changing next_time_run
                return

        # В противном случае пересчитываем время следующего запуска
        self.next_time_run = self.get_next_time_run()

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'


class Log(models.Model):
    """Log model"""
    status_choices = (
        ('success', 'Success'),
        ('error', 'Error'),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Time', **NULLABLE, )
    status = models.CharField(max_length=50, choices=status_choices, verbose_name='Status', **NULLABLE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, verbose_name='Client', **NULLABLE, )
    mailing = models.ForeignKey(MailingCampaign, on_delete=models.CASCADE, verbose_name='Mailing', **NULLABLE, )
    server_response = models.TextField(**NULLABLE, verbose_name='Server response', )

    def __str__(self):
        return f"{self.client} - {self.mailing} - {self.status} - {self.created_at}"

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
