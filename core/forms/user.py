from django import forms
from core.models import User
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.instance.is_active = True

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'cpf', 'email', 'phone',
            'birth_date', 'admission_date', 'photo',
            'is_active', 'is_admin', 'group'
        ]
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
            'admission_date': DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'placeholder': 'exemplo@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'cpf': forms.TextInput(attrs={'maxlength': '11', 'placeholder': 'Apenas números'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        cpf = cpf.replace('.', '').replace('-', '')

        if not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos numéricos.")
        
        qs = User.objects.filter(cpf=cpf)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("CPF já cadastrado.")

        return cpf

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Email já cadastrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        # Se estiver criando um novo usuário ou alterando o email
        if not self.instance.pk or self.instance.email != email:
            if User.objects.filter(username=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Já existe um usuário com esse e-mail como nome de usuário.")

        # Define o username como email (caso não tenha)
        cleaned_data['username'] = email
        return cleaned_data
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone:
            # Remove qualquer formatação
            phone = phone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            if not phone.isdigit():
                raise forms.ValidationError("Telefone deve conter apenas números.")
        return phone
