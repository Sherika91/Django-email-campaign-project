from django import forms

from email_campaign.models import MailingCampaign, Client


class MailingCampaignForm(forms.ModelForm):
    class Meta:
        model = MailingCampaign
        exclude = ('mail_owner', 'next_time_run', 'mail_status',)


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('client_owner',)
