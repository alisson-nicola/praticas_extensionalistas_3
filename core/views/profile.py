from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from core.forms.profile import ProfilePhotoForm, ProfilePasswordForm


@login_required
def profile_view(request):
    user = request.user
    photo_form = ProfilePhotoForm(instance=user)
    password_form = ProfilePasswordForm(user)
    form_open_modal = False  # Flag para abrir modal caso erro na senha

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_photo':
            photo_form = ProfilePhotoForm(request.POST, request.FILES, instance=user)

            if request.POST.get('remove_photo') == 'true':
                user.photo.delete(save=False)
                user.photo = None

            if photo_form.is_valid():
                photo_form.save()
                messages.success(request, 'Foto de perfil atualizada com sucesso.')
                return redirect(reverse('core:profile'))
            else:
                messages.error(request, 'Erro ao atualizar a foto.')

        elif action == 'change_password':
            password_form = ProfilePasswordForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso.')
                return redirect(reverse('core:profile'))
            else:
                form_open_modal = True  # Força abrir a modal em erro de senha

    context = {
        'user': user,
        'photo_form': photo_form,
        'password_form': password_form,
        'form_open_modal': form_open_modal,
        'user_display_fields': [
            {'label': 'Primeiro nome', 'value': user.first_name},
            {'label': 'Sobrenome', 'value': user.last_name},
            {'label': 'Email', 'value': user.email},
            {'label': 'Telefone', 'value': user.phone},
            {'label': 'CPF', 'value': user.cpf},
            {'label': 'Grupo', 'value': user.group.name if user.group else ''},
            {'label': 'Nascimento', 'value': user.birth_date.strftime('%d/%m/%Y') if user.birth_date else ''},
            {'label': 'Admissão', 'value': user.admission_date.strftime('%d/%m/%Y') if user.admission_date else ''},
        ]
    }
    return render(request, 'core/profile/profile_form.html', context)
