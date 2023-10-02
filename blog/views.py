from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['title'] = 'Blog'
        return context

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


@method_decorator(login_required, name='dispatch')
class BlogCreateView(CreateView, LoginRequiredMixin):
    model = Blog
    fields = ['title', 'content', 'image', 'is_published']
    success_url = reverse_lazy('blog:blog-list')

    def form_valid(self, form):
        if form.is_valid():
            new_form = form.save()
            new_form.slug = slugify(new_form.title)
            new_form.save()

            return super().form_valid(form)


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'image', 'is_published']
    success_url = reverse_lazy('blog:blog-list')

    def form_valid(self, form):
        if form.is_valid():
            new_form = form.save()
            new_form.slug = slugify(new_form.title)
            new_form.save()

            return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog-detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_delete_confirm.html'
    success_url = reverse_lazy('blog:blog-list')

    def get_context_data(self, **kwargs):
        context = super(BlogDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Blog Delete'
        return context
