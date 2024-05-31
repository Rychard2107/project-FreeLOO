from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Job


class JobListView(ListView):
    model = Job
    template_name = 'Jobs/Job_list.html'
    context_object_name = 'jobs'
    ordering = ['-created_at']


class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/Job_detail.html'


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['title', 'description']
    template_name = 'Jobs/job_form.html'
    success_url = reverse_lazy('job-list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    fields = ['title', 'description']
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job-list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.posted_by


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job-list')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.posted_by
