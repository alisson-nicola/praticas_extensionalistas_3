from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from core.forms.auth import CustomPasswordResetForm, CustomSetPasswordForm
from core.forms.auth import EmailLoginForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

from django.views.generic.edit import FormView

User = get_user_model()

# -------------------------------
# Login e logout
# -------------------------------

def LoginView(request):
    if request.user.is_authenticated:
        return redirect('core:home_view')

    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('core:home_view')
    else:
        form = EmailLoginForm()

    return render(request, 'core/auth/login.html', {'form': form})


def LogoutView(request):
    logout(request)
    return redirect('core:login')


# -------------------------------
# Recuperação de senha
# -------------------------------

class PasswordResetView(FormView):
    template_name = 'core/auth/password_reset.html'
    success_url = reverse_lazy('core:password_reset_done')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        domain = get_current_site(self.request).domain
        protocol = 'https' if self.request.is_secure() else 'http'
        reset_path = reverse('core:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        reset_link = f"{protocol}://{domain}{reset_path}"

        subject = 'Redefinição de senha - Viener'
        html_content = render_to_string('core/emails/password_reset_email.html', {
            'user': user,
            'protocol': protocol,
            'domain': domain,
            'uid': uid,
            'token': token,
            'reset_link': reset_link,
        })

        # Nome personalizado no remetente
        from_email = 'Viener - Não Responda <teste_dev@viener.com.br>'

        email_message = EmailMultiAlternatives(
            subject=subject,
            body='Clique no link para redefinir sua senha.',
            from_email=from_email,
            to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return super().form_valid(form)


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'core/auth/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'core/auth/password_reset_confirm.html'
    success_url = reverse_lazy('core:password_reset_complete')
    form_class = CustomSetPasswordForm


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'core/auth/password_reset_complete.html'
