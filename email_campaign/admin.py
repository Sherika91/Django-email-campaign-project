from django.contrib import admin

from email_campaign.models import Client, MailingCampaign, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'comment',)
    search_fields = ('email',)


@admin.register(MailingCampaign)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('send_time', 'period', 'mail_status', 'mail_subject', 'body', 'mail_owner')
    search_fields = ('frequency', 'mail_status', 'mail_clients')

    def display_mail_clients(self, obj):
        return ', '.join([client.email for client in obj.mail_clients.all()])

    display_mail_clients.short_description = 'Clients'


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('client', 'created_at', 'mailing', 'status', 'client', 'server_response')
    search_fields = ('status', 'client', 'mailing')


