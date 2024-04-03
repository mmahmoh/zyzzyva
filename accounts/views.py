from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView, UpdateView, DeleteView, CreateView
)

from .forms import (
    LoginForm, ProfileForm, ChangePasswordForm, SignUpForm, PasswordResetForm
)
from .tokens import account_activation_token


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    extra_context = {'title': 'Login'}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('accounts:profile'))
        return super().get(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = 'accounts:login'
    extra_context = {'title': 'Logout'}


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    extra_context = {'title': 'Profile'}


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_update.html'
    form_class = ProfileForm
    extra_context = {'title': 'Update Profile'}

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(
            self.request,
            _(f'{self.request.user} Profile updated successfully')
        )
        return reverse('accounts:profile')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    extra_context = {'title': 'Change Password'}
    form_class = ChangePasswordForm

    def get_success_url(self):
        messages.success(
            self.request,
            _('Password changed successfully')
        )
        return reverse('accounts:profile')


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('accounts:login')
    extra_context = {'title': 'Delete Account'}

    def get_object(self, queryset=None):
        return self.request.user


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    extra_context = {'title': 'Sign Up'}

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # send activation email
        mail_subject = 'Activate your account'
        message = render_to_string(
            'accounts/account_activation_email.html',
            {
                'user': user,
                'domain': get_current_site(self.request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }
        )
        email = EmailMessage(
            mail_subject, message, to=[form.cleaned_data.get('email')]
        )

        if email.send():
            messages.success(
                self.request,
                _(f'{user} Please confirm your email address to complete the '
                  f'registration')
            )
        else:
            messages.error(
                self.request,
                _('An error occurred while sending the activation email')
            )
        return super().form_valid(form)


class SignUpActivateView(View):

    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs.get('uidb64')))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if (user is not None and account_activation_token.check_token(user, kwargs.get('token'))):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(
                request,
                _('Account activated successfully')
            )
        else:
            messages.error(
                request,
                _('Account activation failed')
            )
        return redirect(reverse('accounts:login'))


class PasswordReset(PasswordResetView):
    forme_class = PasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    # subject_template_name = 'accounts/password_reset_subject.txt'
    extra_email_context = {'title': 'Password Reset'}
    success_url = reverse_lazy('accounts:reset_password_done')
    extra_context = {'title': 'Password Reset'}


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    extra_context = {'title': 'Password Reset Done'}


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    extra_context = {'title': 'Password Reset Confirm'}
    success_url = reverse_lazy('accounts:reset_password_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
    extra_context = {'title': 'Password Reset Complete'}


