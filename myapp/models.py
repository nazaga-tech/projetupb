from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

class Candidat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidat_profile')
    candidat_id = models.CharField(max_length=50, primary_key=True)
    telephone = models.CharField(max_length=20)
    nationalite = models.CharField(max_length=50)
    date_naissance = models.DateField()
    cycle_vise = models.CharField(max_length=50)
    niveau_etude = models.CharField(max_length=50)
    Anne_visee = models.IntegerField()
    filiere_visee = models.CharField(max_length=50)
    lettre_motivation = models.FileField(upload_to='lettre_motivation/')
    cv = models.FileField(upload_to='cv/')
    bulletins = models.FileField(upload_to='bulletins/')
    message = models.TextField()
    candidature_acceptee = models.BooleanField(default=False)
    inscription_reussi = models.BooleanField(default=False)
    
    # ajouter les champs email et mot de passe
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
    username=models.CharField(max_length=50)
    
    def __str__(self):
        return f"Candidat n{self.candidat_id} ({self.username})"
    
    def is_accepted(self):
        return self.candidature_acceptee and self.inscription_reussi

    def create_etudiant(self):
        if self.is_accepted():
            etudiant = Etudiant.objects.create(
                etudiant_id=self.id,
                cycle=self.cycle,
                filiere=self.filiere,
                annee=self.annee,
                moyenne_semestre1=self.moyenne_semestre1,
                moyenne_semestre2=self.moyenne_semestre2,
                autorise_passage_classe_superieur=False,
                nationalite=self.user.candidat_profile.nationalite,
                date_naissance=self.user.candidat_profile.date_naissance,
                telephone=self.user.candidat_profile.telephone,
                username=self.user.username,
                email=self.user.email,
                password=self.user.password,
            )
            return etudiant
    
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    admin_id = models.CharField(max_length=50, primary_key=True)
    username=models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"Admin n{self.admin_id} ({self.username})"
    

class Filiere(models.Model):
    nom = models.CharField(max_length=255,primary_key=True)

    def __str__(self):
        return self.nom


class Annee(models.Model):
    Annee = models.CharField(max_length=10,primary_key=True)

    def __str__(self):
        return self.Annee


    

class Etudiant(Candidat):
    etudiant_id = models.CharField(max_length=50, primary_key=True)
    moyenne_semestre1 = models.FloatField()
    moyenne_semestre2 = models.FloatField()
    moyenne_annuelle = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)    
    autorise_passage_classe_superieur = models.BooleanField(default=False)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    Annee = models.ForeignKey(Annee, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.etudiant_id:
            # Si l'id de l'étudiant n'a pas encore été défini, c'est qu'il s'agit d'un nouvel étudiant.
            # On copie les champs hérités du modèle Candidat.
            self.nationalite = self.user.candidat_profile.nationalite
            self.cycle = self.user.candidat_profile.cycle_vise
            self.date_naissance = self.user.candidat_profile.date_naissance
            self.telephone = self.user.candidat_profile.telephone
            self.username = self.user.username
            self.email = self.user.email
            self.password = self.user.password
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Etudiant n{self.etudiant_id} ({self.username})"
    








class Matiere(models.Model):
    nom = models.CharField(max_length=255,primary_key=True)
    coefficient = models.FloatField()

    def __str__(self):
        return self.nom

class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.PROTECT)
    filiere = models.ForeignKey(Filiere, on_delete=models.PROTECT)
    annee = models.ForeignKey(Annee, on_delete=models.PROTECT)
    note_semestre1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    note_semestre2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])

    def __str__(self):
        return f"{self.etudiant.username} - {self.matiere.nom}"
    



class Emploi(models.Model):
        emploi_id = models.CharField(max_length=50, primary_key=True)
        jour = models.CharField(max_length=50)
        heures = models.CharField(max_length=50)
        matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
        filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
        annee = models.ForeignKey(Annee, on_delete=models.CASCADE)

        def __str__(self):
            return f"{self.matiere} - {self.jour} - {self.heures}"
        

class Absence(models.Model):
        etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
        jour = models.CharField(max_length=50)
        heures = models.CharField(max_length=50)
        absence = models.IntegerField(validators=[MaxValueValidator(1)]) 
        filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
        annee = models.ForeignKey(Annee, on_delete=models.CASCADE)

        def __str__(self):
            return f"{self.matiere} - {self.jour} - {self.heures}"