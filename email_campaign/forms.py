from django import forms

from email_campaign.models import MailingCampaign, Client


class MailingCampaignForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.is_staff:
            mail_owner = self.instance.mail_owner
            self.fields['mail_clients'].queryset = Client.objects.filter(client_owner=mail_owner)
        else:
            self.fields['mail_clients'].queryset = Client.objects.filter(client_owner=user)

    class Meta:
        model = MailingCampaign
        exclude = ['mail_owner']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['client_owner']
