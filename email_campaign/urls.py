from django.urls import path
from . import views

from email_campaign.apps import EmailCampaignConfig
from email_campaign.views import index

app_name = EmailCampaignConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('mailing_list/', views.MailingCampaignListView.as_view(), name='mailing_list'),
    path('create/campaign', views.CreateMailingCampaignView.as_view(), name='create_campaign'),
]