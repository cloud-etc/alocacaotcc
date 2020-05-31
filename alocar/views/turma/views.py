from django.contrib.admin.models import LogEntry
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alocar.forms.turma.forms import AddTurmaForm
from alocar.models.alocar.models import Alocar
from alocar.models.turma.models import Turma

import logging

logger = logging.getLogger('django')

def comum(request):
    logEntry = LogEntry.objects.all()
    context = {
        "logEntry": logEntry
    }
    return render(request, "alocar/comum.html", context)

"""
funcao que da acessoa pagin a principal do sistema
e ao dashboard
"""
def home(request):
    context = { }
    return render(request, 'alocar/home.html', context)

"""
consultar turmas sem alocação
"""
def consultarTurmas(request):
    turmas = Turma.objects.raw(
        'SELECT alocar_turma.id, alocar_turma.turma, alocar_turma.curso '
        'FROM alocar_alocar INNER JOIN alocar_turma ON alocar_turma.id <> alocar_alocar.turma_id')

    context = { }
    context['consultarturmas'] = turmas
    return render(request, 'alocar/consultarturmas.html', context)

"""
funcao para cadastrar turma
"""
@login_required
# @permission_required('alocar.add_turma')
def addTurma(request):

    """
    verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.add_turma'):
        return render(request, 'alocar/permissao5.html')

    """
    pesquisa no banco dados
    """
    varios = request.GET.get('varios', None)
    context = {}

    if varios:
        turmas = Turma.objects.filter(turma__icontains=varios) | \
                 Turma.objects.filter(curso__icontains=varios) | \
                 Turma.objects.filter(periodo__icontains=varios) | \
                 Turma.objects.filter(disciplina__icontains=varios) | \
                 Turma.objects.filter(professor__icontains=varios)
    else:
        turmas = Turma.objects.all()


   
    template_name = 'alocar/addturma.html'
    form = AddTurmaForm(request.POST or None)

    if form.is_valid():
        turma = form.cleaned_data['turma']
        curso = form.cleaned_data['curso']
        professor = form.cleaned_data['professor']
        disciplina = form.cleaned_data['disciplina']

        query = Turma.objects.filter(professor=professor) & \
                Turma.objects.filter(disciplina=disciplina)

        if query:
            messages.info(request, 'Essa disciplina já está cadastrada')
            return redirect('alocar:addturma')
        else:
            form.save()
            form = AddTurmaForm()


    paginator = Paginator(turmas, 30)    

    page = request.GET.get('page')

    turmapage = paginator.get_page(page)  

    context['form'] = form
    # context['turmas'] = turmas
    context['turmapage'] = turmapage
    return render(request, template_name, context)





"""
funcao para alterar turma
"""
@login_required
def altTurma(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.change_turma'):
        return render(request, 'alocar/permissao5.html')

    turma = get_object_or_404(Turma, pk=id)
    form = AddTurmaForm(request.POST or None, request.FILES or None, instance=turma)

    values = Alocar.objects.filter(turma=turma)

    if form.is_valid():
        if values:
            messages.info(request, 'NÃO pode ser modificada, porque JÁ está alocada')
            return redirect('alocar:addturma')

        else:
             form.save()
             return redirect('alocar:addturma')

    return render(request, 'alocar/altturma.html', {'form': form})





"""
funcao para deletar turma
"""
@login_required
def delTurma(request, id):
    """
     verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.delete_turma'):
        return render(request, 'alocar/permissao5.html')

    values = Alocar.objects.select_related('turma').filter(turma__id=id)

    if request.method == 'POST':
        if values:
            messages.info(request, 'NÃO pode ser apagada, porque JÁ está alocada')
        else:
            turma = get_object_or_404(Turma, pk=id)
            turma.delete()
        return redirect('alocar:addturma')
    return render(request, 'alocar/delturma.html')


def permissao5(request):
    context = { }
    return render(request, 'alocar/permissao5.html', context)