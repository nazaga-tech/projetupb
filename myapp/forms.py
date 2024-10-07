from django import forms
from .models import Note, Filiere, Annee, Candidat, Matiere,Emploi,Etudiant,Absence


class NoteForm(forms.ModelForm):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all())
    annee_scolaire = forms.ModelChoiceField(queryset=Annee.objects.all())
    etudiant = forms.ModelChoiceField(queryset=Etudiant.objects.none())
    matiere = forms.ModelChoiceField(queryset=Matiere.objects.all())
    note_semestre1 = forms.DecimalField()
    note_semestre2 = forms.DecimalField()

    class Meta:
        model = Note
        fields = ['filiere', 'annee_scolaire', 'etudiant', 'matiere', 'note_semestre1', 'note_semestre2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'filiere' in self.data:
            try:
                filiere_id = int(self.data.get('filiere'))
                annee_id = int(self.data.get('annee'))
                self.fields['etudiant'].queryset = Etudiant.objects.filter(filiere_id=filiere_id, annee_id=annee_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['etudiant'].queryset = self.instance.filiere.Etudiant.filter(annee_id=self.instance.annee_id)

    def __str__(self):
        return self.filiere

        

class EmploiForm(forms.ModelForm):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), required=True)
    annee = forms.ModelChoiceField(queryset=Annee.objects.all(), required=True)
    jour = forms.ChoiceField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')], required=True)
    heures = forms.ChoiceField(choices=[('08h00-10h00', '08h00-10h00'), ('10h00-12h00', '10h00-12h00'), ('14h00-16h00', '14h00-16h00'), ('16h00-18h00', '16h00-18h00')], required=True)
    matiere = forms.ModelChoiceField(queryset=Matiere.objects.all(), required=True)

    class Meta:
        model = Emploi
        fields = ('filiere', 'annee', 'jour', 'heures', 'matiere')

    def __init__(self, *args, **kwargs):
        super(EmploiForm, self).__init__(*args, **kwargs)
        self.fields['jour'].label = 'Jour'
        self.fields['heures'].label = 'Heures'
        self.fields['matiere'].label = 'Matière'
        


class ConsulterEmploiForm(forms.Form):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all())
    annee = forms.ModelChoiceField(queryset=Annee.objects.all())


class ConsulterNotesForm(forms.Form):
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filière'
    )
    annee = forms.ModelChoiceField(
        queryset=Annee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Année'
    )
    etudiant = forms.ModelChoiceField(
        queryset=Etudiant.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Étudiant'
    )



class ConsulterEmploiForm(forms.Form):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all())
    annee = forms.ModelChoiceField(queryset=Annee.objects.all())


class ConsulterAbsencesForm(forms.Form):
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Filière'
    )
    annee = forms.ModelChoiceField(
        queryset=Annee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Année'
    )
    etudiant = forms.ModelChoiceField(
        queryset=Etudiant.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Étudiant'
    )


class AbsencesForm(forms.ModelForm):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), required=True)
    annee = forms.ModelChoiceField(queryset=Annee.objects.all(), required=True)
    etudiant = forms.ModelChoiceField(queryset=Etudiant.objects.none())
    jour = forms.ChoiceField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')], required=True)
    heures = forms.ChoiceField(choices=[('08h00-10h00', '08h00-10h00'), ('10h00-12h00', '10h00-12h00'), ('14h00-16h00', '14h00-16h00'), ('16h00-18h00', '16h00-18h00')], required=True)
    Absence = forms.IntegerField(max_value=1)

    class Meta:
        model = Absence
        fields = ('filiere', 'annee','etudiant', 'jour','heures', 'Absence')

    def __init__(self, *args, **kwargs):
        super(AbsencesForm, self).__init__(*args, **kwargs)
        self.fields['jour'].label = 'Jour'
        self.fields['heures'].label = 'Heures'
        self.fields['Absence'].label = 'Absence'


        if 'filiere' in self.data:
            try:
                filiere_id = int(self.data.get('filiere'))
                annee_id = int(self.data.get('annee'))
                self.fields['etudiant'].queryset = Etudiant.objects.filter(filiere_id=filiere_id, annee_id=annee_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['etudiant'].queryset = self.instance.filiere.Etudiant.filter(annee_id=self.instance.annee_id)

class ValiderAnneeForm(forms.Form):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all())
    annee = forms.ModelChoiceField(queryset=Annee.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['filiere'].widget.attrs.update({'class': 'form-control'})
        self.fields['annee'].widget.attrs.update({'class': 'form-control'})

       
        