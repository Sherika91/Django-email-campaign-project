from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from .models import MailingCampaign, Log

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from email_campaign.forms import MailingCampaignForm


def index(request):
    return render(request, 'email_campaign/index.html')


class MailingCampaignListView(ListView):
    model = MailingCampaign
    template_name = 'email_campaign/campaign_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mailing Campaigns'
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.is_staff:
                queryset = MailingCampaign.objects.all()
            else:
                queryset = super().get_queryset().filter(
                    mail_owner=user.objects.get(pk=user.pk)
                )
        else:
            queryset = super().get_queryset().filter(
                mail_owner=user.objects.get(None)
            )

        return queryset


class CreateMailingCampaignView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = MailingCampaign
    form_class = MailingCampaignForm
    template_name = 'email_campaign/campaign_form.html'
    success_url = reverse_lazy('email_campaign:campaign_list')

