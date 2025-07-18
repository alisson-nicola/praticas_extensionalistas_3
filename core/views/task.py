from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from core.models import Task
from core.forms.task import TaskForm

class TaskListView(ListView):
    model = Task
    template_name = 'core/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']

class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        html = render_to_string('core/includes/task_form.html', {'form': form}, request)
        return JsonResponse({'html': html})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return JsonResponse({'success': True})
        html = render_to_string('core/includes/task_form.html', {'form': form}, request)
        return JsonResponse({'success': False, 'html': html})

class TaskUpdateView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        # Instancia o form com os dados da task para pré-preenchimento
        form = TaskForm(instance=task)
        # Garante que end_date mantenha o valor atual
        if task.end_date:
            form.initial['end_date'] = task.end_date.strftime('%Y-%m-%d')
        html = render_to_string('core/includes/task_form.html', {'form': form}, request)
        return JsonResponse({'html': html})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        html = render_to_string('core/includes/task_form.html', {'form': form}, request)
        return JsonResponse({'success': False, 'html': html})

@require_POST
def update_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    status = request.POST.get('status')
    if status in dict(Task.STATUS_CHOICES):
        task.status = status
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return JsonResponse({'success': True})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    html = render_to_string('core/includes/task_detail.html', {'task': task}, request)
    return JsonResponse({'html': html})
