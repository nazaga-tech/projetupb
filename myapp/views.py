from django.shortcuts import render,redirect
from django.db.models import Avg
#from django.contrib.auth.models import User,login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from email_validator import validate_email,EmailNotValidError
import dns.resolver
import smtplib
from .models import Candidat,Note,Emploi,Admin,Filiere,Annee,Etudiant,Absence
from .forms import NoteForm,EmploiForm,ConsulterEmploiForm,ConsulterNotesForm,AbsencesForm,ConsulterAbsencesForm,ValiderAnneeForm



# Create your views here.
def index(request):
    return render(request,'index.html',)

def register(request):
    if request.method == 'POST':
        telephone=request.POST['telephone']
        nationalite=request.POST.get('country')
        date_naissance = request.POST['birthday']
        cycle_vise = request.POST.get('cycle')
        niveau_etude = request.POST.get('niveauEtude')
        Anne_visee = request.POST.get('AnneeVisee')
        filiere_visee = request.POST.get('filiere')
        lettre_motivation = request.FILES.get('lettreMotivation')
        cv = request.FILES.get('cv')
        bulletins = request.FILES.getlist('bulletins')
        message= request.POST['message']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        candidature_acceptee=False
        inscription_reussi=False

        



        def validate_email_with_smtp(email):
            try:
                # Validate email format using email-validator
                valid = validate_email(email)
                
                # Split email address to get the domain name
                domain = email.split('@')[1]
                
                # MX record lookup to get the SMTP server for the domain
                mx_records = dns.resolver.query(domain, 'MX')
                mx_record = str(mx_records[0].exchange)
                
                # SMTP request to verify email existence
                smtp = smtplib.SMTP(mx_record)
                smtp.connect(mx_record)
                smtp.helo()
                smtp.mail('racemidio21@gmail.com')
                status, _ = smtp.rcpt(email)
                if status == 250:
                    return True
                else:
                    return False
            except EmailNotValidError:
                return False
    


        is_valid_email = validate_email_with_smtp(email)

        if not is_valid_email :
            messages.error(request,'Cette adresse e-mail n\'est pas valide')
            return redirect('candidature.html')
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Cet email est deja utilise')
                return redirect('candidature.html')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)   
                user.set_password(request.POST['password'])    
                user.save()
                
                candidat = Candidat.objects.create(
                telephone=telephone,
                nationalite=nationalite,
                date_naissance=date_naissance,
                cycle_vise=cycle_vise,
                niveau_etude=niveau_etude,
                Anne_visee=Anne_visee,
                filiere_visee=filiere_visee,
                lettre_motivation=lettre_motivation,
                cv=cv,
                bulletins =bulletins,
                message=message,
                candidature_acceptee=candidature_acceptee,
                inscription_reussi=inscription_reussi,
                user=user,
                )
                candidat.save()    

                messages.success(request, 'Votre candidature a été enregistrée avec succès.')
                return redirect('candidature.html')
        else:
            messages.info(request,'vos Mots de passe sont differents')
            return redirect('candidature.html')

    else:
        return render(request,'candidature.html',)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(emai=email, password= password)
        candidat=candidat
        if user is not None:#already_registred
            login(request, user) 
            request.session[user.email] = user.email
            if role == 'admin'and role=='professeur':
                return redirect('portAdmin')
            elif role == 'professeur':
                return redirect('portAdmin')
            elif role == 'etudiant':
                if not candidat.candidature_acceptee:
                    messages.error(request, 'Votre candidature est en attente')
                else:
                    return redirect ('port_etu.html')
            else:
                return redirect('login')
        else:
            messages.info(request,'informations non correspondants')
            return redirect('login')    

    else:
        return render(request,'connexion.html')
    



def portEtu(request):
    return render(request,'port_etu.html',)


def portAdmin(request):
    return render(request,'portAdmin.html',)

def gestion_candidatures(request):
    candidats = Candidat.objects.all()
    if request.method == 'POST':
        candidat_id = request.POST.get('candidat_id')
        candidat = Candidat.objects.get(id=candidat_id)
        decision = request.POST.get('decison')
        if decision == 'accepte':
            candidat.candidature_acceptee = True
            candidat.save()
        else:
            candidat.candidature_acceptee = False
            candidat.save()
        return redirect('gestion_candidatures')
    else:
        return render(request, 'gestion_candidature.html', {'candidats': candidats})

def gestion_inscriptions(request):
        candidats_acceptes = Candidat.objects.filter(candidature_acceptee=True)
        candidats = Candidat.objects.all()

        if request.method == 'POST':
            candidat_accepte_id = request.POST.get('candidat_accepte_id')
            candidat_accepte = Candidat.objects.get(id=candidat_accepte_id)
            inscription_reussi = request.POST.get('inscription_reussi')
            if inscription_reussi == 'OUI':
                candidat_accepte.inscription_reussi = True
                candidat_accepte.save()
            else:
                candidat_accepte.inscription_reussi = False
                candidat_accepte.save()

            for candidat in candidats:
                if candidat.is_accepted():
                    etudiant = candidat.create_etudiant()
                    print(f"L'étudiant {etudiant.etudiant_id} a été créé avec succès !")
                else:
                    print("Le candidat n'est pas encore accepté ou inscrit.")                
            return redirect('gestion_inscriptions')
        else:
            return render(request, 'gestion_inscription.html', {'candidat_acceptes': candidats_acceptes})



        

def genie_informatique(request):
    return render(request,'genie-informatique.html',)

def genie_civil(request):
    return render(request,'genie-civil.html',)
def genie_Industriel_Logistique(request):
    return render(request,'genie-Industrielle&Logistique.htm',)

def management(request):
    return render(request,'management.htm',)



def gestion_notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            messages.success(request, 'Note ajoutée avec succès')
            return redirect('gestion_notes.htm')
    else:
        form = NoteForm()
    return render(request, 'gestion_notes.html', {'form': form})


class AjaxView(View):
    def get_etudiants(self, request):
        filiere_id = request.GET.get('filiere_id')
        annee_scolaire_id = request.GET.get('annee_scolaire_id')
        etudiants = Etudiant.objects.filter(filiere_id=filiere_id, annee_scolaire_id=annee_scolaire_id)
        etudiants = {}
        for etudiant in etudiants:
            etudiants[etudiant.id] = etudiant.nom + ' ' + etudiant.prenom
        return JsonResponse(etudiants)

    def get(self, request, *args, **kwargs):
        return self.get_etudiants(request)




def gestion_emploi_du_temps(request):
    filieres = Filiere.objects.all()
    annees = Annee.objects.all()
    form = EmploiForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            emploi = form.save(commit=False)
            emploi.filiere = form.cleaned_data['filiere']
            emploi.annee = form.cleaned_data['annee']
            emploi.save()
            form = EmploiForm(initial={'filiere': emploi.filiere, 'annee': emploi.annee})
            message = "Enregistre !"

    else:
        message = ""
        form = EmploiForm()

    return render(request, 'gestion_emploi_du_temps.html', {'form': form, 'filieres': filieres, 'annees': annees, 'message': message})


def consulter_emploi(request):
    if request.method == "POST":
        form = ConsulterEmploiForm(request.POST)
        if form.is_valid():
            filiere = form.cleaned_data["filiere"]
            annee = form.cleaned_data["annee"]
            emploi = Emploi.objects.filter(filiere=filiere, annee=annee)
            return render(request, "consulterEmploi.html", {"form": form, "emploi": emploi})
    else:
        form = ConsulterEmploiForm()
    return render(request, "consulterEmploi.html", {"form": form})


def consulter_notes(request):
    form = ConsulterNotesForm(request.POST or None)
    notes = None

    if request.method == 'POST' and form.is_valid():
        filiere = form.cleaned_data['filiere']
        annee = form.cleaned_data['annee']
        etudiant = form.cleaned_data['etudiant']
        notes = Note.objects.filter(etudiant=etudiant)

        # Mettre à jour le queryset du champ etudiant en fonction de la filière et de l'année
        form.fields['etudiant'].queryset = Etudiant.objects.filter(filiere=filiere, annee=annee)

        context = {'form': form, 'notes': notes}
        return render(request, 'consulterNotes.html', context)
    else:
        form = ConsulterNotesForm()
    return render(request, "consulterNotes.html", {"form": form})


def reinitialiser_emploi(request, filiere_id, annee_id):
    filiere = Filiere.objects.get(id=filiere_id)
    annee = Annee.objects.get(id=annee_id)
    Emploi.objects.filter(filiere_id=filiere.id, annee_id=annee.id).delete()
    messages.success(request, "L'emploi du temps de la filière et de l'année sélectionnée a été réinitialisé avec succès. Vous pouvez maintenant le remplir à nouveau.")
    context = {
        'filiere': filiere,
        'annee': annee,
    }
    return render(request, 'gestion_emploi_du_temps.html', context)



def reinitialiser_absences(request, filiere_id, annee_id,etudiant_id):
    Absence.objects.filter(filiere_id=filiere_id, annee_id=annee_id,etudiant_id=etudiant_id).delete()
    messages.success(request, "Les absences hebdomadaires de cet etudiant ont été réinitialisé avec succès. Vous pouvez maintenant les remplir à nouveau.")
    return redirect('gestion_absences.html', filiere_id=filiere_id, annee_id=annee_id,etudiant_id=etudiant_id)



def gestion_absences(request):
    if request.method == 'POST':
        form = AbsencesForm(request.POST)
        if form.is_valid():
            Absence = form.save(commit=False)
            Absence.save()
            messages.success(request, 'Absence ajoutée avec succès')
            return redirect('gestion_absences.html')
    else:
        form = AbsencesForm()
    return render(request, 'gestion_absences.html', {'form': form})   


def consulter_absences(request):
    form = ConsulterAbsencesForm(request.POST or None)
    Absences = None

    if request.method == 'POST' and form.is_valid():
        filiere = form.cleaned_data['filiere']
        annee = form.cleaned_data['annee']
        etudiant = form.cleaned_data['etudiant']
        Absences = Absence.objects.filter(etudiant=etudiant)

        # Mettre à jour le queryset du champ etudiant en fonction de la filière et de l'année
        form.fields['etudiant'].queryset = Etudiant.objects.filter(filiere=filiere, annee=annee)

        context = {'form': form, 'Absences': Absences}
        return render(request, 'consulter_absences.html', context)
    else:
        form =ConsulterAbsencesForm()
    return render(request, "consulter_absences.html", {"form": form})


@login_required
def emploi_etudiant(request):
    # Récupérer l'étudiant connecté
    etudiant = request.user.etudiant

    # Récupérer l'emploi du temps de l'étudiant connecté
    emploi = Emploi.objects.filter(filiere=etudiant.filiere, annee=etudiant.annee)

    # Envoyer le contexte au template
    context = {'emploi': emploi}

    return render(request, 'port_etu.html', context)



@login_required
def consultation_notes_par_etudiant(request):
    # Récupérer l'étudiant connecté
    etudiant = request.user.etudiant

    # Récupérer toutes les notes de l'étudiant dans toutes les matières
    notes = Note.objects.filter(etudiant=etudiant)

    context = {
        'notes': notes,
    }

    return render(request, 'port_etu.html', context)


@login_required
def consultation_absences_par_etudiant(request):
    # Récupérer l'étudiant connecté
    etudiant = request.user.etudiant

    # Récupérer toutes les notes de l'étudiant dans toutes les matières
    absences = Absence.objects.filter(etudiant=etudiant)

    context = {
        'absences': absences,
    }

    return render(request, 'port_etu.html', context)





def valider_annee(request):
    if request.method == 'POST':
        form = ValiderAnneeForm(request.POST)
        if form.is_valid():
            filiere = form.cleaned_data['filiere']
            annee = form.cleaned_data['annee']
            etudiants = Etudiant.objects.filter(filiere=filiere, annee_scolaire=annee)
            total_etudiants = etudiants.count()
            somme_moyenne_semestre1 = 0
            somme_moyenne_semestre2 = 0
            somme_moyenne_annuelle = 0
            for etudiant in etudiants:
                notes_semestre1 = Note.objects.filter(etudiant=etudiant, matiere__semestre=1)
                notes_semestre2 = Note.objects.filter(etudiant=etudiant, matiere__semestre=2)
                moyenne_semestre1 = notes_semestre1.aggregate(Avg('note_semestre1'))['note_semestre1__avg']
                moyenne_semestre2 = notes_semestre2.aggregate(Avg('note_semestre2'))['note_semestre2__avg']
                moyenne_annuelle = (moyenne_semestre1+moyenne_semestre2) / 2
                somme_moyenne_semestre1 += moyenne_semestre1
                somme_moyenne_semestre2 += moyenne_semestre2
                somme_moyenne_annuelle += moyenne_annuelle

            if total_etudiants > 0:
                moyenne_generale_semestre1 = somme_moyenne_semestre1 / total_etudiants
                moyenne_generale_semestre2 = somme_moyenne_semestre2 / total_etudiants
                moyenne_generale_annuelle = somme_moyenne_annuelle / total_etudiants
            else:
                moyenne_generale_semestre1 = 0
                moyenne_generale_semestre2 = 0
                moyenne_generale_annuelle = 0

            context = {
                'etudiants': etudiants,
                'moyenne_generale_semestre1': moyenne_generale_semestre1,
                'moyenne_generale_semestre2': moyenne_generale_semestre2,
                'moyenne_generale_annuelle': moyenne_generale_annuelle,
                'total_etudiants': total_etudiants,
                'form': form
            }
            return render(request, 'validation_annee.html', context)
    else:
        form =  ValiderAnneeForm()
        return render(request, 'validation_annee.html', {'form': form})
    