from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Personne(models.Model):
    nom = models.CharField(max_length=50, blank=False, null=False)
    prenom = models.CharField(max_length=50, blank=False, null=False)
    localite = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom

    @staticmethod
    def find_all():
        return Personne.objects.all()

    @staticmethod
    def find_personne_by_user(user):
        try:
            return Personne.objects.get(user=user)
        except Exception:
            return None

    @staticmethod
    def find_by_id(an_id):
        return Personne.objects.get(pk=an_id)


class Categorie(models.Model):
    libelle = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.libelle


class LivreAdmin(admin.ModelAdmin):
    search_fields = ['titre']
    raw_id_fields = ('categorie', )


class Livre(models.Model):
    LANGUE = (
        ('FR', 'Français'),
        ('ENG', 'Anglais')
    )

    titre = models.CharField(max_length=100, blank=False, null=False)
    langue = models.CharField(max_length=5, choices=LANGUE, default='FR')
    categorie = models.ForeignKey(Categorie, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modification = models.DateTimeField(auto_now=True, blank=True, null=True)
    remarque = models.TextField(blank=True, null=True)

    @property
    def proprietaires(self):
        return Proprietaire.objects.filter(livre=self)

    @staticmethod
    def find_all():
        return Livre.objects.all().order_by('titre')

    @staticmethod
    def find_livre(an_id):
        return Livre.objects.get(pk=an_id)

    def auteurs_livres(self):
        return AuteurLivre.objects.filter(livre=self)

    @staticmethod
    def find_last_by_user(user):
        liste_livre = []
        if user.is_authenticated():
            person = Personne.find_personne_by_user(user)
            l = Proprietaire.objects.filter(personne=person).order_by('-livre__date_modification')

            for p in l:
                liste_livre.append(p.livre)

        return liste_livre

    @staticmethod
    def find_all_by_user(user):
        liste_livre = []
        if user.is_authenticated():
            person = Personne.find_personne_by_user(user)
            l = Proprietaire.objects.filter(personne=person)

            for p in l:
                liste_livre.append(p.livre)

        return liste_livre

    @staticmethod
    def find_all_lecture_by_user(user):
        liste_livre = []
        if user.is_authenticated():
            person = Personne.find_personne_by_user(user)
            l = Lecture.objects.filter(personne=person).order_by('-date_modification')
            return l

        return liste_livre
    
    def __str__(self):
        return self.titre

    @staticmethod
    def find_lecture(livre_id, user):
        person = Personne.find_personne_by_user(user)
        livre = Livre.objects.get(pk=livre_id)
        try:
            return Lecture.objects.get(personne=person, livre=livre)
        except Exception:
            return None

    @staticmethod
    def find_by_etat_lecture(etat_lecture, user):
        person = Personne.find_personne_by_user(user)
        livres = []
        if etat_lecture:
            lecture_liste = Lecture.objects.filter(personne=person)
            for lecture in lecture_liste:
                livres.append(lecture.livre)
            return livres
        else:
            liste_livre = Livre.objects.all()
            for livre in liste_livre:
                if not Lecture.objects.filter(personne=person):
                    livres.append(livre)
            return livres

    @property
    def auteurs_livres_str(self):
        auteurs = []
        for al in AuteurLivre.objects.filter(livre=self):
            auteurs.append(al.auteur)
        s = ""
        cpt = 0
        for a in auteurs:
            if cpt > 0:
                s = s + " / "
            s = s + str(a)
            cpt = cpt + 1
        return s

    @staticmethod
    def find_by_proprietaire(personne_id):
        personne = None
        if personne_id:
            personne = Personne.find_by_id(personne_id)

        livres = []
        if personne:
            # proprietaire
            list_proprietaire = Proprietaire.objects.filter(personne=personne)
            for l in list_proprietaire:
                livres.append(l.livre)

        return livres

    @staticmethod
    def find_by_auteur(auteur_id):
        auteur = None
        if auteur_id:
            auteur = Auteur.find_auteur(auteur_id)
        livres = []
        if auteur:
            list_livre_auteur = AuteurLivre.objects.filter(auteur=auteur).order_by('livre__titre')
            for l in list_livre_auteur:
                livres.append(l.livre)
        return livres

    @staticmethod
    def find_by_titre(titre):
        return Livre.objects.filter(titre__icontains=titre)

    @staticmethod
    def is_lu(livre, user):
        person = Personne.find_personne_by_user(user)
        livre = Livre.objects.get(pk=livre.id)
        try:
            if Lecture.objects.get(personne=person, livre=livre):
                return True
        except Exception:
            return False
        return False


class Lecteur(models.Model):
    livre = models.ForeignKey(Livre, blank=False, null=False)
    personne = models.ForeignKey(Personne, blank=False, null=False)

    def __str__(self):
        return self.livre + ", " + self.personne

    @staticmethod
    def find_all():
        return Lecteur.objects.all()

    @staticmethod
    def find_by_personne(personne):
        return Lecteur.objects.filter(personne=personne)

    @staticmethod
    def find_distinct():
        q = Lecteur.objects.values('personne').distinct()
        personnes = []
        for engt in q:
            p = Personne.find_by_id(engt.get('personne'))
            if p:
                personnes.append(p)
        return personnes


class AuteurAdmin(admin.ModelAdmin):
    search_fields = ['nom']


class Auteur(models.Model):
    nom = models.CharField(max_length=100, blank=False, null=False)
    prenom = models.CharField(max_length=100, blank=True, null=True)

    @staticmethod
    def find_all():
        return Auteur.objects.all().order_by('nom', 'prenom')

    @staticmethod
    def find_auteur(an_id):
        return Auteur.objects.get(pk=an_id)

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom


class AuteurLivreAdmin(admin.ModelAdmin):
    raw_id_fields = ('livre', 'auteur')


class AuteurLivre(models.Model):
    livre = models.ForeignKey(Livre, blank=False, null=False)
    auteur = models.ForeignKey(Auteur, blank=False, null=False)

    @staticmethod
    def find_auteur_livre(an_id):
        return AuteurLivre.objects.get(pk=an_id)

    @staticmethod
    def find_auteur_livre_by_auteur(auteur):
        return AuteurLivre.objects.filter(auteur=auteur)
    
    def __str__(self):
        return self.livre.titre + ", " + self.auteur.nom


class Location(models.Model):
    AVIS = (
        ('CHOUETTE', 'Chouette'),
        ('BOF', 'Bof'),
        ('NUL', 'Nul'),
        ('SUPER', 'Super'),
        )
    lecteur = models.ForeignKey('Lecteur')
    livre = models.ForeignKey('Livre')
    date_debut_location = models.DateField(auto_now=False, auto_now_add=False)
    date_fin_location = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    remarque = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.lecteur.nom + ", " + self.livre.titre


class ProprietaireAdmin(admin.ModelAdmin):
    raw_id_fields = ('personne', 'livre')
    list_filter = ('livre',)
    search_fields = ['livre']


class Proprietaire(models.Model):
    personne = models.ForeignKey(Personne)
    livre = models.ForeignKey(Livre)

    def __str__(self):
            return self.personne.nom + ", " + self.livre.titre

    def est_disponible(self):
        emprunt = Emprunt.objects.filter(proprietaire=self, date_retour__isnull=True)
        if emprunt:
            return False
        else:
            return True

    @staticmethod
    def find_emprunt_by_proprietaire(proprietaire):
        try:
            return Emprunt.objects.get(proprietaire=proprietaire)
        except Exception:
            return None

    @staticmethod
    def find_emprunt_en_cours_by_proprietaire(proprietaire):
        try:
            return Emprunt.objects.get(proprietaire=proprietaire, date_retour__isnull=True)
        except Exception:
            return None

    def emprunt_courant(self):
        emprunts = Emprunt.objects.filter(proprietaire=self, personne=self.personne, date_retour__isnull=True)
        if emprunts:
            return emprunts[0].id
        else:
            return None

    @staticmethod
    def find_by_personne(personne):
        return Proprietaire.objects.filter(personne=personne)

    @staticmethod
    def find_distinct():
        q = Proprietaire.objects.values('personne').distinct()
        personnes = []
        for engt in q:
            p = Personne.find_by_id(engt.get('personne'))
            if p:
                personnes.append(p)

        return personnes


class Lecture(models.Model):
    personne = models.ForeignKey(Personne, blank=False, null=False)
    livre = models.ForeignKey(Livre, blank=False, null=False)
    date_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modification = models.DateTimeField(auto_now=True, blank=True, null=True)
    remarque = models.TextField(blank=True, null=True)

    def __str__(self):
            return self.personne.nom + ", " + self.livre.titre

    @staticmethod
    def find_by_id(an_id):
        return Livre.objects.get(pk=an_id)

    @staticmethod
    def find_all():
        return Lecture.objects.all()

    @staticmethod
    def find_last_by_user(user):
        person = Personne.find_personne_by_user(user)
        l = Lecture.objects.filter(personne=person).order_by('-livre__date_modification')
        liste_livre = []
        for p in l:
            liste_livre.append(p.livre)
        return liste_livre

    @staticmethod
    def find_all_by_user(user):
        person = Personne.find_personne_by_user(user)
        l = Lecture.objects.filter(personne=person)
        liste_livre = []
        for p in l:
            liste_livre.append(p.livre)
        return liste_livre

    @staticmethod
    def find_distinct():
        q = Lecture.objects.values('personne').distinct()
        personnes = []
        for engt in q:
            p = Personne.find_by_id(engt.get('personne'))
            if p:
                personnes.append(p)
        return personnes

    @staticmethod
    def find_all_by_user_livre(user):
        person = Personne.find_personne_by_user(user)
        return Lecture.objects.filter(personne=person)

    @staticmethod
    def find_lecture(livre, personne):
        try:
            return Lecture.objects.get(personne=personne, livre=livre)
        except Exception:
            return None


class Emprunt(models.Model):
    personne = models.ForeignKey(Personne, blank=False, null=False)
    proprietaire = models.ForeignKey(Proprietaire, blank=False, null=False)
    date_emprunt = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    date_retour = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)

    @staticmethod
    def find_emprunt_courant_by_user(user):
        personne = Personne.find_personne_by_user(user)
        return Emprunt.objects.filter(personne=personne, date_retour__isnull=True)

    @staticmethod
    def find_locations(user):
        personne = Personne.find_personne_by_user(user)
        list_propriete = Proprietaire.find_by_personne(personne)
        locations = []
        for p in list_propriete:
            loc = Emprunt.objects.filter(proprietaire=p, date_retour__isnull=True)
            for l in loc:
                locations.append(l)
        return locations

    def __str__(self):
            return self.personne.nom + ", " + self.proprietaire.personne.nom
