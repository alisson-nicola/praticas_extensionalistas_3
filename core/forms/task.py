from django import forms
from core.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao', 'end_date', 'status']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }
