from django.urls import path
from . import views

from email_campaign.apps import EmailCampaignConfig
from email_campaign.views import index

app_name = EmailCampaignConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('campaign/contacts/', views.contacts, name='contacts'),
    path('campaign/', views.CampaignListView.as_view(), name='campaign-list'),
    path('campaign/create/', views.CampaignCreateView.as_view(), name='campaign-create'),
    path('campaign/<int:pk>/detail/', views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('campaign/<int:pk>/update/', views.CampaignUpdateView.as_view(), name='campaign-update'),
    path('campaign/<int:pk>/delete/', views.CampaignDeleteView.as_view(), name='campaign-delete'),
    path('client/', views.ClientListView.as_view(), name='client-list'),
    path('client/crete/', views.ClientCreateView.as_view(), name='client-create'),
    path('client/<int:pk>/detail/', views.ClientDetailView.as_view(), name='client-detail'),
    path('client/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client-update'),
    path('client/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client-delete'),

]
