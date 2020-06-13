from django.contrib import admin
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

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('horario',)
    search_fields = ('horario',)
    list_filter = ('horario',)


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('bloco','sala','capmaxima','disponivel','internet','projetor','computador')
    search_fields = ('bloco__bloco','sala',)
    list_filter = ('sala','disponivel')
    ordering = ('sala',)
    autocomplete_fields = ['bloco']


    # def delete_model(self, request, obj):
    #     values = Alocar.objects.select_related('sala').filter(sala__id=id)

    #     if request.method == 'POST':
    #         if values:
    #             messages.info(request, 'NÃO pode ser excluida, pois está alocada')
    #         else:
    #             obj = get_object_or_404(Sala, pk=id)
    #             obj.delete()

    

@admin.register(Bloco)
class BlocoAdmin(admin.ModelAdmin):
    list_display = ('bloco',)
    search_fields = ('bloco',)
    ordering = ('bloco',)






