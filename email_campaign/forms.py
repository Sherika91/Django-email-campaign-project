from django import forms

from email_campaign.models import MailingCampaign, Client


class MailingCampaignForm(forms.ModelForm):

    class Meta:
        model = MailingCampaign
        fields = '__all__'
        exclude = ['mail_owner']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['client_owner']
