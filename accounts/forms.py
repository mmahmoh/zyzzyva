from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm, PasswordResetForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        fields = ['email', 'password', 'captcha']


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('E-mail'),
        disabled=True,
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'phone']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_('Old Password'),
        widget=forms.PasswordInput,
    )
    new_password1 = forms.CharField(
        label=_('New Password'),
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label=_('Confirm New Password'),
        widget=forms.PasswordInput,
    )

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']


class SignUpForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'phone', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_('Email already exists'))
        return email


class ResetPasswordForm(PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        fields = ['email', 'captcha']
