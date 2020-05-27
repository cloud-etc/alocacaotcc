import xlwt
from datetime import datetime
from excel_response import ExcelResponse
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Count
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from alocar.forms import AddBlocoForm, AddHorarioForm, AddSalaForm, AddAlocForm, AddTurmaForm
from usuarios.forms import User
from .models import Alocar, Bloco, Horario, Sala, Turma

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
        return render(request, 'alocar/permissao.html')

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
        return render(request, 'alocar/permissao.html')

    turma = get_object_or_404(Turma, pk=id)
    form = AddTurmaForm(request.POST or None, request.FILES or None, instance=turma)

    values = Alocar.objects.filter(turma=turma)

    if form.is_valid():
        if values:
            turma.save()
            messages.info(request, 'NÃO pode ser alterada, porque JÁ está alocada')
            return redirect('alocar:addturma')

        else:
             form.save()
             return redirect('alocar:addturma')

    return render(request, 'alocar/altturma.html', {'form': form})





"""
funcao para deletar turma
"""
@login_required
# @permission_required('alocar.delete_turma',)
def delTurma(request, id):

    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """

    if not request.user.has_perm('alocar.delete_turma'):        
        return render(request, 'alocar/permissao.html')

    values = Alocar.objects.select_related('turma').filter(turma__id=id)

    if request.method == 'POST':
        if values:
            messages.info(request, 'NÃO pode ser excluida, porque JÁ está alocada')
        else:
            turma = get_object_or_404(Turma, pk=id)
            turma.delete()
        return redirect('alocar:addturma')
    return render(request, 'alocar/delturma.html')





"""
funcao para cadastrar sala
"""
@login_required
def addSala(request):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.add_sala'):
        return render(request, 'alocar/permissao.html')

    varios = request.GET.get('varios', None)
    context = {}
    if varios:
        salas =  Sala.objects.filter(bloco__bloco__icontains=varios) | \
                 Sala.objects.filter(sala__icontains=varios)
    else:
        salas = Sala.objects.all().filter(disponivel=True)

    template_name = 'alocar/addsala.html'
    form = AddSalaForm(request.POST or None)

    if form.is_valid():
        sala = form.cleaned_data['sala']
        query = Sala.objects.filter(sala=sala)

        if query:        
            messages.info(request, 'Essa Sala já está cadastrada')
            # form.save()
            # form = AddSalaForm()
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
        return render(request, 'alocar/permissao.html')

    sala = get_object_or_404(Sala, pk=id)
    form = AddSalaForm(request.POST or None, request.FILES or None, instance=sala)

    if form.is_valid():

        sala = Alocar.objects.select_related('sala').filter(sala__id=id)

        if sala:
            sala = form.save(commit=False)
            sala.save()
            return redirect('alocar:addsala')
        else:
            form.save()
            return redirect('alocar:addsala')

    return render(request, 'alocar/altsala.html', {'form': form})






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
        return render(request, 'alocar/permissao.html')


    values = Alocar.objects.select_related('sala').filter(sala__id=id)

    if request.method == 'POST':
        if values:
            messages.info(request, 'NÃO pode ser excluida, pois está alocada')
        else:
            sala = get_object_or_404(Sala, pk=id)
            sala.delete()
        return redirect('alocar:addsala')
    return render(request, 'alocar/delsala.html')



"""
funcao para cadastrar alocacao
"""
@login_required
# @permission_required('alocar.view_alocar')
def listSalaTurma(request, *args, **kwargs):
    """
    verifica se o usuario tem perimissao, para fazer a operacao
    """
    varios = request.GET.get('varios', None)

    if varios:
        turmapage = Turma.objects.filter(turma__icontains=varios) | \
                    Turma.objects.filter(curso__icontains=varios) | \
                    Turma.objects.filter(periodo__icontains=varios) | \
                    Turma.objects.filter(disciplina__icontains=varios) | \
                    Turma.objects.filter(professor__icontains=varios)
    else:
        # turmapage = Turma.objects.all()
        turmapage = Turma.objects.select_related()


    varios1 = request.GET.get('varios1', None)

    if varios1:
        salapage =  Sala.objects.filter(bloco__bloco__icontains=varios1) | \
                    Sala.objects.filter(sala__icontains=varios1)
    else:
        salapage =  Sala.objects.filter(

            disponivel=True
        )
        

    alocar = Alocar.objects.all()

    context = {}
    template_name = 'alocar/listsalaturma.html'

    form = AddAlocForm(request.POST or None)

    if form.is_valid():
        
        turma = form.cleaned_data['turma']
        sala = form.cleaned_data['sala']
        dia = form.cleaned_data['dia']
        horario = form.cleaned_data['horario']

        alocacao = form.save(commit=False)
        alocacao.user = request.user    

        if alocacao.maior():
            messages.info(
                request, 'Quantidade de alunos é maior do que a capacidade da sala')
            return redirect('alocar:listalocacao')


        if alocacao.turma_computador():
            if alocacao.sala_computador():
                messages.info(
                    request, 'Essa turma precisa de computador')
                return redirect('alocar:listalocacao')

        
        if alocacao.turma_internet():
            if alocacao.sala_internet():
                messages.info(
                request, 'Essa turma precisa de internet')
                return redirect('alocar:listalocacao')


        if alocacao.turma_projetor():
            if alocacao.sala_projetor():
                messages.info(
                    request, 'Essa turma precisa de projetor')
                return redirect('alocar:listalocacao')


        query = Alocar.objects.filter(dia=dia) & \
                Alocar.objects.filter(horario=horario) & \
                Alocar.objects.filter(sala=sala)
        if query:
            messages.info(request, 'Essa sala já está alocada para esse dia e horário')
            return redirect('alocar:listalocacao')


        query = Alocar.objects.filter(dia=dia) & \
                Alocar.objects.filter(horario=horario) & \
                Alocar.objects.filter(turma__professor=turma.professor)
        if query:
            messages.info(
                request, 'Esse Professor já está em uma turma para esse dia e horário')
            return redirect('alocar:listalocacao')


        query = Alocar.objects.filter(dia=dia) & \
            Alocar.objects.filter(horario=horario) & \
            Alocar.objects.filter(turma=turma)
        if query:
            messages.info(
                request, 'Essa turma já está alocada para esse dia e horário')
            return redirect('alocar:listalocacao')


        query = Alocar.objects.filter(turma=turma) & \
                Alocar.objects.filter(sala=sala)
        if query:
            messages.info(request, 'Essa turma já está alocada')
            return redirect('alocar:listalocacao')

        else:
            alocacao.save()
            form = AddAlocForm()
            return redirect('alocar:listalocacao')



    paginator = Paginator(turmapage, 30)    
    page = request.GET.get('page')
    turmapage = paginator.get_page(page)

    paginator1 = Paginator(salapage, 30)
    page1 = request.GET.get('page')
    salapage = paginator1.get_page(page1)

    context['form'] = form
    context['turmapage'] = turmapage
    context['salapage'] = salapage
    return render(request, template_name, context)


"""
funcao para listar as alocacoes
"""


@login_required
# @permission_required('alocar.view_alocar',)
def listAlocacao(request):
    """
    pesquisa no banco dados
    """
    logger.info('Acessaram a listagem de alocação')
    varios = request.GET.get('varios', None)
    context = {}
    if varios:
        alocacoes = Alocar.objects.filter(turma__curso__icontains=varios) | \
                    Alocar.objects.filter(turma__periodo__icontains=varios) | \
                    Alocar.objects.filter(turma__disciplina__icontains=varios) | \
                    Alocar.objects.filter(turma__professor__icontains=varios) | \
                    Alocar.objects.filter(dia__icontains=varios) | \
                    Alocar.objects.filter(horario__horario__icontains=varios) | \
                    Alocar.objects.filter(sala__sala__icontains=varios)
    else:
        alocacoes = Alocar.objects.all()

    paginator = Paginator(alocacoes, 30)

    page = request.GET.get('page')

    alocapage = paginator.get_page(page)

    context = {'alocacoes': alocacoes, 'alocapage': alocapage}
    return render(request, 'alocar/listalocacao.html', context)



"""
funcao para alterar alocacao
"""
@login_required
# @permission_required('alocar.change_alocar',)
def altAlocacao(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.change_alocar'):
        return render(request, 'alocar/permissao.html')

    alocacao = get_object_or_404(Alocar, pk=id)

    form = AddAlocForm(request.POST or None, request.FILES or None,
                       instance=alocacao)

    if form.is_valid():

        alocacao = form.save(commit=False)
        alocacao.turma = form.cleaned_data['turma']
        alocacao.sala = form.cleaned_data['sala']
        alocacao.dia = form.cleaned_data['dia']
        alocacao.horario = form.cleaned_data['horario']

        if alocacao.maior():
            messages.info(
                request, 'Quantidade de alunos é maior do que a capacidade da sala')
            return redirect('alocar:listalocacao')

        if alocacao.turma_computador():
            if alocacao.sala_computador():
                messages.info(
                    request, 'Essa turma precisa de computador')
                return redirect('alocar:listalocacao')

        if alocacao.turma_internet():
            if alocacao.sala_internet():
                messages.info(
                    request, 'Essa turma precisa de internet')
                return redirect('alocar:listalocacao')

        if alocacao.turma_projetor():
            if alocacao.sala_projetor():
                messages.info(
                    request, 'Essa turma precisa de projetor')
                return redirect('alocar:listalocacao')

        query = Alocar.objects.filter(dia=alocacao.dia) & \
                Alocar.objects.filter(sala=alocacao.sala) & \
                Alocar.objects.filter(horario=alocacao.horario)
        if query:
            messages.info(request, 'Essa sala já está alocada para esse dia e horário')
            return redirect('alocar:listalocacao')

        # query = Alocar.objects.filter(dia=alocacao.dia) & \
        #         Alocar.objects.filter(horario=alocacao.horario) & \
        #         Alocar.objects.filter(turma__professor=alocacao.turma.professor)
        # if query:
        #     messages.info(
        #         request, 'Esse Professor já está em uma turma para esse dia e horário')
        #     return redirect('alocar:listalocacao')

        query = Alocar.objects.filter(dia=alocacao.dia) & \
                Alocar.objects.filter(horario=alocacao.horario) & \
                Alocar.objects.filter(turma=alocacao.turma)
        if query:
            messages.info(
                request, 'Essa turma já está alocada para esse dia e horário')
            return redirect('alocar:listalocacao')

        query = Alocar.objects.filter(turma=alocacao.turma) & \
                Alocar.objects.filter(sala=alocacao.sala)
        if query:
            messages.info(request, 'Essa turma já está alocada')
            return redirect('alocar:listalocacao')

        query = Alocar.objects.filter(turma=alocacao.turma)


        if query:
            alocacao.save()
            return redirect('alocar:listalocacao')
        else:
            form.save()
            return redirect('alocar:listalocacao')

    return render(request, 'alocar/altalocacao.html', {'form': form})




"""
funcao para deletar alocacao
"""
@login_required
# @permission_required('alocar.deletar_alocar',)
def delAlocacao(request, id):
    """
     verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.delete_alocar'):
        return render(request, 'alocar/permissao.html')

    context = {}
    alocar = get_object_or_404(Alocar, pk=id)

    if request.user.is_superuser:
        if request.method == 'POST':
            alocar.delete()
            return redirect('alocar:listalocacao')

    else:        

        if alocar.user == request.user:
            if request.method == 'POST':
                alocar.delete()
                return redirect('alocar:listalocacao')

        else:
            if not alocar.user == request.user:
                messages.info(
                request, 'Você NÃO pode apagar essa alocação. Porque foi feita por outro usuário')
                return redirect('alocar:listalocacao')
            

    context['alocar'] = alocar
    return render(request, 'alocar/delalocacao.html')



"""
funcao para cadastrar bloco
"""
@login_required
# @permission_required('alocar.add_bloco',)
def addBloco(request):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.add_bloco'):
        return render(request, 'alocar/permissao.html')


    blocos = Bloco.objects.all().order_by('bloco')
    context = {}
    template_name = 'alocar/addbloco.html'
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
# @permission_required('alocar.change_bloco',)
def altBloco(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
       """
    if not request.user.has_perm('alocar.change_bloco'):
        return render(request, 'alocar/permissao.html')

    bloco = get_object_or_404(Bloco, pk=id)
    form = AddBlocoForm(request.POST or None, request.FILES or None, instance=bloco)
    values = Sala.objects.select_related('bloco').filter(bloco__id=id)
    if form.is_valid():
        if values:
            messages.info(request, 'NÃO pode ser editado, já faz parte de algum relacionamento')
        else:
            form.save()
        return redirect('alocar:addbloco')

    return render(request, 'alocar/altbloco.html', {'form': form})




"""
funcao para deletar bloco
"""
@login_required
def delBloco(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.delete_bloco'):
        return render(request, 'alocar/permissao.html')


    values = Sala.objects.select_related('bloco').filter(bloco__id=id)
    if request.method == 'POST':
        if values:
            messages.info(request, 'NÃO pode ser apagado, já faz parte de algum relacionamento')
        else:
            bloco = get_object_or_404(Bloco, pk=id)
            bloco.delete()
        return redirect('alocar:addbloco')
    return render(request, 'alocar/delbloco.html')





"""
funcao para cadastrar horario
"""
@login_required
def addHorario(request):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
    """
    if not request.user.has_perm('alocar.add_horario'):
        return render(request, 'alocar/permissao.html')


    horarios = Horario.objects.all().order_by('horario')
    context = {}
    template_name = 'alocar/addhorario.html'
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
        return render(request, 'alocar/permissao.html')


    horario = get_object_or_404(Horario, pk=id)
    form = AddHorarioForm(request.POST or None, request.FILES or None, instance=horario)
    values = Alocar.objects.select_related('horario').filter(horario__id=id)
    if form.is_valid():
        if values:
            messages.info(request, 'NÃO pode ser editado, já faz parte de alguma alocação')
        else:
            form.save()
        return redirect('alocar:addhorario')

    return render(request, 'alocar/althorario.html', {'form': form})






"""
funcao para deletar horario
"""
@login_required
def delHorario(request, id):
    """
        verifica se o usuario tem perimissao, para fazer a operacao
       """
    if not request.user.has_perm('alocar.delete_horario'):
        return render(request, 'alocar/permissao.html')

    horario = get_object_or_404(Horario, pk=id)
    values = Alocar.objects.select_related('horario').filter(horario__id=id)
    if request.method == 'POST':
        if values:
            messages.info(request, 'NÃO pode ser apagado, já faz parte de alguma alocação')
        else:
            horario.delete()
        return redirect('alocar:addhorario')

    return render(request, 'alocar/delhorario.html', {"horario":horario})







"""
funcao que exporta relatório excel, csv
"""
def export_alocacoes_xls(request):
    MDATA = datetime.now().strftime('%d-%m-%Y')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="alocacoes.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Alocacoes')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['BLOCO','SALA','CURSO','PERIODO','DISCIPLINA','PROFESSOR','DIA','HORARIO']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Alocar.objects.all().values_list('sala__bloco__bloco','sala__sala','turma__curso','turma__periodo','turma__disciplina','turma__professor','dia','horario__horario')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_segunda(request):
    objs = Alocar.objects.filter(dia="segunda")
    return ExcelResponse(objs)

# def export_segunda(request, *segunda):
#     MDATA = datetime.now().strftime('%d-%m-%Y')
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="alocacoes.xls"'
#
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Alocacoes')
#
#     # Sheet header, first row
#     row_num = 0
#
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#
#     columns = ['BLOCO','SALA','CURSO','PERIODO','DISCIPLINA','PROFESSOR','DIA','HORARIO']
#
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)
#
#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()
#
#     # rows = Alocar.objects.all().values_list('sala__bloco__bloco','sala__sala','turma__curso','turma__periodo','turma__disciplina','turma__professor','dia','horario__horario')
#     rows = Alocar.objects.filter(dia=segunda).values_list('sala__bloco__bloco','sala__sala','turma__curso','turma__periodo','turma__disciplina','turma__professor','dia','horario__horario')
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)
#
#     wb.save(response)
#     return response


def export_terca(request):
    MDATA = datetime.now().strftime('%d-%m-%Y')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="alocacoes.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Alocacoes')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['BLOCO','SALA','CURSO','PERIODO','DISCIPLINA','PROFESSOR','DIA','HORARIO']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Alocar.objects.all().values_list('sala__bloco__bloco','sala__sala','turma__curso','turma__periodo','turma__disciplina','turma__professor','dia','horario__horario')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_quarta(request):
    MDATA = datetime.now().strftime('%d-%m-%Y')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="alocacoes.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Alocacoes')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['BLOCO','SALA','CURSO','PERIODO','DISCIPLINA','PROFESSOR','DIA','HORARIO']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Alocar.objects.all().values_list('sala__bloco__bloco','sala__sala','turma__curso','turma__periodo','turma__disciplina','turma__professor','dia','horario__horario')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_quinta(request):
    MDATA = datetime.now().strftime('%d-%m-%Y')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="alocacoes.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Alocacoes')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['BLOCO','SALA','CURSO','PERIODO','DISCIPLINA','PROFESSOR','DIA','HORARIO']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Alocar.objects.all().values_list('sala__bloco__bloco','sala__sala','turma__curso','turma__periodo','turma__disciplina','turma__professor','dia','horario__horario')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_sexta(request):
    MDATA = datetime.now().strftime('%d-%m-%Y')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="alocacoes.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Alocacoes')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['BLOCO','SALA','CURSO','PERIODO','DISCIPLINA','PROFESSOR','DIA','HORARIO']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Alocar.objects.all().values_list('sala__bloco__bloco','sala__sala','turma__curso','turma__periodo','turma__disciplina','turma__professor','dia','horario__horario')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_sabado(request):
    MDATA = datetime.now().strftime('%d-%m-%Y')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="alocacoes.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Alocacoes')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['BLOCO','SALA','CURSO','PERIODO','DISCIPLINA','PROFESSOR','DIA','HORARIO']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Alocar.objects.all().values_list('sala__bloco__bloco','sala__sala','turma__curso','turma__periodo','turma__disciplina','turma__professor','dia','horario__horario')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def permissao(request):
    context = { }
    return render(request, 'alocar/permissao.html', context)
