from django.urls import path
from . import views
# je viens d'ajouter
from django.contrib.auth import views as auth_views
from .views import  AjaxView

urlpatterns = [
    path('', views.index, name ='index'),
    path('register/', views.register, name ='register'),   
    path('login/', views.login, name ='login'),
    path('port_etu.html/', views.portEtu, name ='portEtu.html'),
    path('portAdmin/', views.portAdmin, name ='portAdmin'),
    path('portAdmin/gestion_candidatures/', views.gestion_candidatures, name ='gestion_candidatures'),
    path('portAdmin/gestion_inscriptions/', views.gestion_inscriptions, name ='gestion_inscriptions'),
    path('genie_informatique/', views.genie_informatique, name ='genie_informatique'),
    path('genie_civil/', views.genie_civil, name ='genie_civil'),
    path('genie_Industriel&Logistique/', views.genie_Industriel_Logistique, name ='genie_Industriel&Logistique'),
    path('management/', views.management, name ='management'),
    path('portAdmin/valider_annee/', views.valider_annee, name ='valider_annee'),
    path('portAdmin/gestion_notes/', views.gestion_notes, name ='gestion_notes'),
    path('ajax/etudiants/', AjaxView.as_view(), name='ajax_etudiants'),
    path('portAdmin/gestion_emploi_du_temps/', views.gestion_emploi_du_temps, name ='gestion_emploi_du_temps'),
    path('reinitialiser_emploi/<int:filiere_id>/<int:annee_id>/', views.reinitialiser_emploi, name='reinitialiser_emploi'),
    path('portAdmin/gestion_absences/', views.gestion_absences, name ='gestion_absences'),
    path('portAdmin/consulter_emploi/', views.consulter_emploi, name ='consulter_emploi'),
    path('portAdmin/consulterNotes.html/', views.consulter_notes, name ='consulterNotes.html'),
    path('portAdmin/consulter_absences/', views.consulter_absences, name ='consulter_absences'),
]
