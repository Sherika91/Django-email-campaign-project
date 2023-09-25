from django.urls import path
from . import views

from email_campaign.apps import EmailCampaignConfig
from email_campaign.views import index

app_name = EmailCampaignConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('campaign/', views.CampaignListView.as_view(), name='campaign-list'),
    path('campaign/create/', views.CampaignCreateView.as_view(), name='campaign-create'),
    path('campaign/<int:pk>/detail/', views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('campaign/<int:pk>/update/', views.CampaignUpdateView.as_view(), name='campaign-update'),
    path('campaign/<int:pk>/delete/', views.CampaignDeleteView.as_view(), name='campaign-delete'),

]
