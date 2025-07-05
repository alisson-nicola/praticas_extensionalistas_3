from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from core.forms.user import UserForm
from core.models import User
from core.decorators import permission_required
from django.conf import settings


@login_required
@permission_required('usuarios')
def user_list(request):
    users = User.objects.all()
    return render(request, 'core/users/user_list.html', {'users': users})


@login_required
@permission_required('usuarios')
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                password = get_random_string(10)
                user = form.save(commit=False)
                user.set_password(password)
                if not user.username:
                    user.username = user.email
                user.save()

                subject = 'Boas-vindas ao Sistema Viener'
                message = render_to_string('core/emails/welcome_email.html', {
                    'user': user,
                    'password': password
                })

                # Nome personalizado no remetente
                from_email = 'Viener - Não Responda <teste_dev@viener.com.br>'

                send_mail(
                    subject,
                    '',
                    from_email,
                    [user.email],
                    fail_silently=False,
                    html_message=message
                )

                messages.success(request, "Usuário criado com sucesso e e-mail enviado.")
                return redirect('core:user_list')
            except Exception as e:
                messages.error(request, f"Erro ao salvar usuário: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserForm()
    return render(request, 'core/users/user_form.html', {'form': form, 'user_obj': None})


@login_required
@permission_required('usuarios')
def user_edit(request, pk):
    user_instance = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user_instance)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                if not user.username:
                    user.username = user.email
                user.save()
                messages.success(request, "Usuário atualizado com sucesso.")
                return redirect('core:user_list')
            except Exception as e:
                messages.error(request, f"Erro ao atualizar usuário: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserForm(instance=user_instance)
    return render(request, 'core/users/user_form.html', {'form': form, 'edit_mode': True, 'user_obj': user_instance})
