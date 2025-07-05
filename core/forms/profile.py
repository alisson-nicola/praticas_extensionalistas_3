from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from core.models import User


class ProfilePhotoForm(forms.ModelForm):
    remove_photo = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['photo']


class ProfilePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Senha atual',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-md border-gray-300 shadow-sm px-3 py-2 focus:ring-[#2d4739] focus:border-[#2d4739] sm:text-sm',
            'placeholder': 'Digite sua senha atual',
            'id': 'id_current_password'
        })
    )
    new_password1 = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-md border-gray-300 shadow-sm px-3 py-2 focus:ring-[#2d4739] focus:border-[#2d4739] sm:text-sm',
            'placeholder': 'Digite sua nova senha',
            'id': 'id_new_password1'
        })
    )
    new_password2 = forms.CharField(
        label='Confirme a nova senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-md border-gray-300 shadow-sm px-3 py-2 focus:ring-[#2d4739] focus:border-[#2d4739] sm:text-sm',
            'placeholder': 'Confirme a nova senha',
            'id': 'id_new_password2'
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.user.check_password(current_password):
            raise forms.ValidationError("A senha atual está incorreta.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("new_password2", "As senhas não coincidem.")

            try:
                password_validation.validate_password(password1, self.user)
            except ValidationError as e:
                self.add_error("new_password1", e.messages)

        return cleaned_data

    def save(self):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.save()
        return self.user
