from django.urls import path
from django.contrib.auth import views as auth_views
from .views import user_signup, user_login, user_logout, dashboard, verify_email, delete_account, edit_profile

urlpatterns = [
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='User/password_reset.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='User/password_reset_done.html'), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='User/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='User/password_reset_complete.html'), name='password_reset_complete'),
    path("verify/", verify_email, name="verify_email"),  # No token needed
    path("verify/<str:token>/", verify_email, name="verify_email_token"),  # Handles direct verification links
    path("delete-account/", delete_account, name="delete_account"),
    path("edit-profile/", edit_profile, name="edit_profile"),
]
