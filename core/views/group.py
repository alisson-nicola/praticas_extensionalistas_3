from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms.group import GroupForm
from core.models import Group, User
from core.decorators import permission_required

@login_required
@permission_required('grupos')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'core/groups/group_list.html', {'groups': groups})

@login_required
@permission_required('grupos')
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo criado com sucesso.')
            return redirect('core:group_list')
    else:
        form = GroupForm()
    return render(request, 'core/groups/group_form.html', {'form': form})

@login_required
@permission_required('grupos')
def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo atualizado com sucesso.')
            return redirect('core:group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'core/groups/group_form.html', {'form': form})

@login_required
@permission_required('grupos')
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if User.objects.filter(group=group).exists():
        messages.error(request, 'Não é possível excluir este grupo, pois está relacionado a usuários.')
    else:
        group.delete()
        messages.success(request, 'Grupo excluído com sucesso.')
    return redirect('core:group_list')
