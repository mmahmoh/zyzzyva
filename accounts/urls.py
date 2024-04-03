from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('change/password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('delete/account/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.SignUpActivateView.as_view(), name='activate-account'),
    path('reset/password/', views.PasswordReset.as_view(), name='reset_password'),
    path('reset/password/done/', views.PasswordResetDone.as_view(), name='reset_password_done'),
    path('reset/password/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='reset_password_confirm'),
    path('reset/password/complete/', views.PasswordResetComplete.as_view(), name='reset_password_complete'),
]