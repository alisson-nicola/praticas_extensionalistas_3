from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm
)

User = get_user_model()

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("E-mail não encontrado.")

            if not user.check_password(password):
                raise forms.ValidationError("Senha incorreta.")

            if not user.is_active:
                raise forms.ValidationError("Usuário inativo.")

            cleaned_data['user'] = user

        return cleaned_data

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Nenhuma conta com esse e-mail foi encontrada.")
        return email

class CustomSetPasswordForm(SetPasswordForm):
    pass  # Usa comportamento padrão (nova senha e confirmação)