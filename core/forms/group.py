# core/forms/group.py
from django import forms
from core.models import Group, Screen

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Screen.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissões disponíveis"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].label_from_instance = lambda obj: obj.name
