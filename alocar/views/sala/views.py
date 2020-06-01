from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alocar.forms.sala.forms import AddSalaForm
from alocar.models.alocar.models import Alocar
from alocar.models.sala.models import Sala


"""
funcao para cadastrar sala
"""
@login_required
def addSala(request):
    """
     verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.add_sala'):
        return render(request, 'alocar/permissao1.html')

    """
    filtro de pesquisa 
    """
    varios = request.GET.get('varios', None)
    context = {}
    if varios:
        salas =  Sala.objects.filter(bloco__bloco__icontains=varios) | \
                 Sala.objects.filter(sala__icontains=varios)
    else:
        salas = Sala.objects.all().filter(disponivel=True)


    template_name = 'sala/addsala.html'
    form = AddSalaForm(request.POST or None)

    if form.is_valid():
        sala = form.cleaned_data['sala']
        query = Sala.objects.filter(sala=sala)

        if query:        
            messages.info(request, 'Sala com essa descrição já está cadastrada')
            return redirect('alocar:addsala')
        else:
            form.save()
            form = AddSalaForm()
            return redirect('alocar:addsala')

    paginator = Paginator(salas, 30)    

    page = request.GET.get('page')

    salapage = paginator.get_page(page)  

    context['form'] = form
    context['salapage'] = salapage
    return render(request, template_name, context)




"""
funcao para alterar sala
"""
@login_required
def altSala(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.change_sala'):
        return render(request, 'alocar/permissao1.html')

    sala = get_object_or_404(Sala, pk=id)
    form = AddSalaForm(request.POST or None, request.FILES or None, instance=sala)

    if form.is_valid():

        sala = Alocar.objects.select_related('sala').filter(sala__id=id)

        if sala:
            messages.info(request, 'NÃO pode ser modificada, pois está alocada')
            return redirect('alocar:addsala')
        else:
            form.save()
            return redirect('alocar:addsala')

    return render(request, 'sala/altsala.html', {'form': form})




"""
funcao para deletar sala
"""
@login_required
# @permission_required('alocar.delete_sala',)
def delSala(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.delete_sala'):
        return render(request, 'alocar/permissao1.html')


    values = Alocar.objects.select_related('sala').filter(sala__id=id)

    if request.method == 'POST':
        if values:
            messages.info(request, 'NÃO pode ser apagada, pois está alocada')
        else:
            sala = get_object_or_404(Sala, pk=id)
            sala.delete()
        return redirect('alocar:addsala')
    return render(request, 'sala/delsala.html')



def permissao4(request):
    context = { }
    return render(request, 'alocar/permissao4.html', context)

