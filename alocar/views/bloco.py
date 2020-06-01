from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from alocar.forms.bloco import AddBlocoForm
from alocar.models.sala import Sala
from alocar.models.bloco import Bloco
"""
funcao para cadastrar bloco
"""
@login_required
def addBloco(request):
    """
    verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.add_bloco'):
        return render(request, 'alocar/permissao2.html')


    blocos = Bloco.objects.all().order_by('bloco')
    context = {}
    template_name = 'bloco/addbloco.html'
    form = AddBlocoForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = AddBlocoForm()

    context['form'] = form
    context['blocos'] = blocos
    return render(request, template_name, context)


"""
funcao para alterar bloco
"""
@login_required
def altBloco(request, id):
    """
     verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.change_bloco'):
        return render(request, 'alocar/permissao2.html')

    bloco = get_object_or_404(Bloco, pk=id)
    form = AddBlocoForm(request.POST or None, request.FILES or None, instance=bloco)
    values = Sala.objects.select_related('bloco').filter(bloco__id=id)
    if form.is_valid():
        if values:
            messages.info(request, 'NÃO pode ser editado, já faz parte de algum relacionamento')
        else:
            form.save()
        return redirect('alocar:addbloco')

    return render(request, 'bloco/altbloco.html', {'form': form})


"""
funcao para deletar bloco
"""
@login_required
def delBloco(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.delete_bloco'):
        return render(request, 'alocar/permissao2.html')


    values = Sala.objects.select_related('bloco').filter(bloco__id=id)
    if request.method == 'POST':
        if values:
            messages.info(request, 'NÃO pode ser apagado, já faz parte de algum relacionamento')
        else:
            bloco = get_object_or_404(Bloco, pk=id)
            bloco.delete()
        return redirect('alocar:addbloco')
    return render(request, 'bloco/delbloco.html')


def permissao2(request):
    context = { }
    return render(request, 'alocar/permissao2.html', context)