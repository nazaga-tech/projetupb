from django.contrib import admin
from .models import Candidat, Admin,Etudiant,Filiere,Annee,Matiere,Note,Absence

admin.site.register(Candidat)
admin.site.register( Admin)
admin.site.register( Filiere)
admin.site.register( Annee)
admin.site.register(Absence)
admin.site.register( Matiere)


class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('etudiant_id', 'username', 'email', 'password', 'nationalite', 'date_naissance', 'telephone', 'filiere', 'Annee', 'moyenne_semestre1', 'moyenne_semestre2', 'moyenne_annuelle','autorise_passage_classe_superieur')
    list_filter = ('filiere', 'Annee', 'autorise_passage_classe_superieur')
    search_fields = ('etudiant_id', 'nationalite', 'filiere__nom', 'Annee__annee')

    def filiere(self, obj):
        return obj.filiere.nom

    def Annee(self, obj):
        return obj.Annee.annee

    filiere.admin_order_field = 'filiere__nom'
    Annee.admin_order_field = 'Annee__annee'

admin.site.register(Etudiant, EtudiantAdmin)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('filiere', 'annee', 'etudiant', 'matiere', 'note_semestre1', 'note_semestre2')
    list_filter = ('filiere', 'annee', 'etudiant','matiere')
    search_fields = ('filiere', 'annee', 'etudiant','matiere','note_semestre1', 'note_semestre2')


admin.site.register( Note,NoteAdmin)