from django.db import models
from config import settings

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    """Client model"""
    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Client owner',
                                     **NULLABLE),
    email = models.EmailField(max_length=150, unique=True),
    first_name = models.CharField(max_length=100),
    last_name = models.CharField(max_length=100),
    comment = models.TextField(**NULLABLE),

    def __str__(self):
        return f"{self.email} ({self.first_name} {self.last_name})"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class MailingCampaign(models.Model):
    """Campaign model"""
    frequency_choice = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ),

    status_choice = (
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
    ),

    send_time = models.TimeField(verbose_name='Send time'),
    frequency = models.CharField(max_length=20, choices=frequency_choice),
    mail_status = models.CharField(max_length=20, choices=status_choice, default='created', verbose_name='Status'),
    mail_clients = models.ManyToManyField(Client,  verbose_name='Clients', **NULLABLE),
    mail_subject = models.CharField(max_length=100, verbose_name='Subject'),
    body = models.TextField(verbose_name='Body'),
    mail_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Campaign owner',
                                   **NULLABLE),

    def __str__(self):
        return f"{self.mail_subject} в {self.send_time} ({self.frequency}"

    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'
        permissions = [
            ('set_mail_status', 'Set mail status')
        ]


class Log(models.Model):
    """Log model"""
    status_choices = (
        ('success', 'Success'),
        ('error', 'Error'),
    ),

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Time'),
    status = models.CharField(max_length=50, choices=status_choices, verbose_name='Status'),
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client'),
    mailing = models.ForeignKey(MailingCampaign, on_delete=models.CASCADE, verbose_name='Mailing'),
    server_response = models.TextField(**NULLABLE, verbose_name='Server response'),

    def __str__(self):
        return f"{self.client} - {self.mailing} - {self.status} - {self.created_at}"

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
