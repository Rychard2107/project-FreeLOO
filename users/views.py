from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    second_form_class = UserUpdateForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = self.second_form_class(instance=self.request.user)
        if 'profile_form' not in context:
            context['profile_form'] = self.form_class(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.second_form_class(request.POST, instance=request.user)
        profile_form = self.form_class(request.POST, request.FILES, instance=self.request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return self.form_valid(profile_form)
        else:
            return self.form_invalid(profile_form)
