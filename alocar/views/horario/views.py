
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alocar.forms.horario.forms import AddHorarioForm
from alocar.models.alocar.models import Alocar, Horario

"""
funcao para cadastrar horario
"""
@login_required
def addHorario(request):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.add_horario'):
        return render(request, 'alocar/permissao1.html')


    horarios = Horario.objects.all().order_by('horario')
    context = {}
    template_name = 'horario/addhorario.html'
    form = AddHorarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = AddHorarioForm()
    context['form'] = form
    context['horarios'] = horarios
    return render(request, template_name, context)




"""
funcao para alterar horario
"""
@login_required
def altHorario(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
       """
    if not request.user.has_perm('alocar.change_horario'):
        return render(request, 'alocar/permissao1.html')


    horario = get_object_or_404(Horario, pk=id)
    form = AddHorarioForm(request.POST or None, request.FILES or None, instance=horario)
    values = Alocar.objects.select_related('horario').filter(horario__id=id)
    if form.is_valid():
        if values:
            messages.info(request, 'NÃO pode ser editado, já faz parte de alguma alocação')
        else:
            form.save()
        return redirect('alocar:addhorario')

    return render(request, 'horario/althorario.html', {'form': form})



"""
funcao para deletar horario
"""
@login_required
def delHorario(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
       """
    if not request.user.has_perm('alocar.delete_horario'):
        return render(request, 'alocar/permissao1.html')

    horario = get_object_or_404(Horario, pk=id)
    values = Alocar.objects.select_related('horario').filter(horario__id=id)
    if request.method == 'POST':
        if values:
            messages.info(request, 'NÃO pode ser apagado, já faz parte de alguma alocação')
        else:
            horario.delete()
        return redirect('alocar:addhorario')

    return render(request, 'horario/delhorario.html', {"horario":horario})


def permissao3(request):
    context = { }
    return render(request, 'alocar/permissao3.html', context)

