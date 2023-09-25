from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from users.models import User
from .models import MailingCampaign, Log

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from email_campaign.forms import MailingCampaignForm


def index(request):
    return render(request, 'email_campaign/index.html')


class CampaignListView(ListView):
    model = MailingCampaign
    template_name = 'email_campaign/campaign_list.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignListView, self).get_context_data(**kwargs)
        context['title'] = 'Mailing Campaigns'
        return context

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists() or user.is_superuser:
            queryset = super().get_queryset()
        else:
            queryset = super().get_queryset().filter(
                mail_owner=user.pk
            )
        return queryset


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = MailingCampaign
    form_class = MailingCampaignForm
    template_name = 'email_campaign/campaign_form.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Mailing Campaign Creation'
        return context

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save()
        self.object.mail_owner = user
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('email_campaign:campaign-detail', args=[self.object.pk])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingCampaign
    form_class = MailingCampaignForm
    template_name = 'email_campaign/campaign_form.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Edit Campaign'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('email_campaign:campaign-detail', args=[self.object.pk])


class CampaignDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingCampaign
    template_name = 'email_campaign/campaign_confirm_delete.html'
    success_url = reverse_lazy('email_campaign:campaign-list')

    def get_context_data(self, **kwargs):
        context = super(CampaignDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete Campaign'
        return context


class CampaignDetailView(DetailView):
    model = MailingCampaign
    template_name = 'email_campaign/campaign_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Campaign Details'
        return context

