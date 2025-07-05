from django.urls import path
from core.views.auth import (
    LoginView, LogoutView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from core.views.home import home_view
from core.views.redirects import redirect_to_login
from core.views.group import group_list, group_create, group_edit, group_delete
from core.views.user import user_list, user_create, user_edit
from core.views.profile import profile_view

app_name = 'core'

urlpatterns = [
    path('', redirect_to_login, name='root'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('home/', home_view, name='home_view'),

    # URLs de recuperação de senha
    path('esqueci-a-senha/', PasswordResetView.as_view(), name='password_reset'),
    path('senha-enviada/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('redefinir-senha/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('senha-alterada/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Grupos
    path('groups/', group_list, name='group_list'),
    path('groups/create/', group_create, name='group_create'),
    path('groups/<int:pk>/edit/', group_edit, name='group_edit'),
    path('groups/<int:pk>/delete/', group_delete, name='group_delete'),

    # Usuários
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:pk>/edit/', user_edit, name='user_edit'),

    # Perfil
    path('profile/', profile_view, name='profile'),

]
