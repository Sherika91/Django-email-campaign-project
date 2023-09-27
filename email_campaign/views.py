from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator

from users.models import User
from .models import MailingCampaign, Log, Client

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from email_campaign.forms import MailingCampaignForm, ClientForm


def index(request):
    return render(request, 'email_campaign/index.html')


@method_decorator(login_required, name='dispatch')
class CampaignListView(ListView, LoginRequiredMixin):
    model = MailingCampaign
    template_name = 'email_campaign/campaign_list.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignListView, self).get_context_data(**kwargs)
        context['title'] = 'Mailing Campaigns'
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            queryset = MailingCampaign.objects.all()
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
        return redirect(get_absolute_url())

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


class CampaignDetailView(DetailView, LoginRequiredMixin):
    model = MailingCampaign
    template_name = 'email_campaign/campaign_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Campaign Details'
        return context


@method_decorator(login_required, name='dispatch')
class ClientListView(ListView, LoginRequiredMixin):
    model = User
    template_name = 'email_campaign/client_list.html'

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['title'] = 'Clients'
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.is_staff:
                queryset = User.objects.all()
            else:
                queryset = super().get_queryset().filter(
                    pk=user.pk
                )
        else:
            queryset = super().get_queryset().filter(
                pk=None
            )
        return queryset


class ClientCreateView(CreateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    template_name = 'email_campaign/client_form.html'

    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Clients Creation'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client_owner = self.request.user
        self.object.save()
        return redirect(self.get_absolute_url())


class ClientUpdateView(UpdateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    template_name = 'email_campaign/client_form.html'

    def get_context_data(self, **kwargs):
        context = super(ClientUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Edit Clients'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.client_owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class ClientDetailView(DetailView, LoginRequiredMixin):
    model = Client
    template_name = 'email_campaign/client_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Clients Details'
        return context


class ClientDeleteView(DeleteView, LoginRequiredMixin):
    model = Client
    template_name = 'email_campaign/client_confirm_delete.html'
    success_url = reverse_lazy('email_campaign:client-list')

    def get_context_data(self, **kwargs):
        context = super(ClientDeleteView, self).get_context_data()
        context['title'] = 'Delete Client'
        return context
