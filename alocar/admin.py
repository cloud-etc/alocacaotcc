from django.contrib import admin, messages
from django.shortcuts import redirect

from alocar.models.alocarModel import Alocar
from alocar.models.blocoModel import Bloco
from alocar.models.horarioModel import Horario
from alocar.models.salaModel import Sala
from alocar.models.turmaModel import Turma
from import_export.admin import ImportExportModelAdmin


@admin.register(Turma)
class TurmaAdmin(ImportExportModelAdmin):
    list_display = ('turma','curso','periodo','disciplina','alocada','professor','qtdalunos','internet','projetor','computador')
    search_fields = ('turma','curso','professor','disciplina')
    list_filter = ('curso','periodo','professor','disciplina')
    readonly_fields = ('alocada',)
    actions = ['delete_selected']

    def save_model(self, request, obj, form, change):
        values = Alocar.objects.select_related('turma').filter(turma__id=obj.id)
        if values:
            messages.info(request, 'NÃO pode ser alterada, já faz parte de algum relacionamento')
        else:
            obj.save()

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('horario',)
    search_fields = ('horario',)
    list_filter = ('horario',)

    def save_model(self, request, obj, form, change):
        values = Alocar.objects.select_related('horario').filter(horario__id=obj.id)
        if values:
            messages.info(request, 'NÃO pode ser alterada, já faz parte de algum relacionamento')
        else:
            obj.save()



@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('bloco','sala','capmaxima','disponivel','internet','projetor','computador')
    search_fields = ('bloco__bloco','sala',)
    list_filter = ('sala','disponivel')
    ordering = ('sala',)
    autocomplete_fields = ['bloco']

    def save_model(self, request, obj, form, change):
        values = Alocar.objects.select_related('sala').filter(sala__id=obj.id)
        if values:
            messages.info(request, 'NÃO pode ser alterada, já faz parte de algum relacionamento')
        else:
            obj.save()


    

@admin.register(Bloco)
class BlocoAdmin(admin.ModelAdmin):
    list_display = ('bloco',)
    search_fields = ('bloco',)
    ordering = ('bloco',)


    def save_model(self, request, obj, form, change):
        values = Sala.objects.select_related('bloco').filter(bloco__id=obj.id)
        if values:
            messages.success(request, 'NÃO pode ser alterado, já faz parte de algum relacionamento')
        else:
            obj.save()

admin.site.disable_action('delete_selected')



