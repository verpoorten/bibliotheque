from django.db import models
from django.contrib.auth.models import User

class Personne(models.Model):
    nom    = models.CharField(max_length = 100, blank = False, null = False)
    prenom = models.CharField(max_length = 100, blank = False, null = False)
    user        = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom

    def find_all():
        return Personne.objects.all()

    def find_all_exclude_user(current_user):
        return Personne.objects.all().exclude(user = current_user)

    @staticmethod
    def find_personne_by_user(user):
        return Personne.objects.get(user=user)


class Categorie(models.Model):
    libelle = models.CharField(max_length = 100, blank = False, null = False)

    def __str__(self):
        return self.libelle


class Livre(models.Model):
    LANGUE = (
        ('FR','Français'),
        ('ENG','Anglais')
    )

    titre      = models.CharField(max_length = 100, blank = False, null = False)
    langue     = models.CharField(max_length=5,choices = LANGUE, default = 'FR')
    categorie  = models.ForeignKey(Categorie, blank = True, null = True)

    def proprietaires(self):
        return Proprietaire.objects.filter(livre = self)

    @staticmethod
    def find_all():
        return Livre.objects.all().order_by('titre')

    @staticmethod
    def find_livre(id):
        return Livre.objects.get(pk=id)

    def auteurs_livres(self):
        return AuteurLivre.objects.filter(livre=self)

    @staticmethod
    def find_all_by_user(user):
        person = Personne.find_personne_by_user(user)
        print(person)
        l= Proprietaire.objects.filter(personne=person)
        liste_livre=[]
        for p in l:
            liste_livre.append(p.livre)

        return liste_livre

    def __str__(self):
        return self.titre

    @staticmethod
    def find_lecture(livre_id,user):
        person = Personne.find_personne_by_user(user)
        livre = Livre.objects.get(pk=livre_id)
        try:
            return Lecture.objects.get(personne=person,livre= livre)
        except:
            return None

    def auteurs_livres_str(self):
        s = ""
        cpt=0
        for al in  AuteurLivre.objects.filter(livre=self):
            print(al.livre)
            if cpt>0:
                s = s + ", " + al.auteur
            else:
                s = al.auteur
            cpt=cpt+1
        return s

    def find_by_proprietaire_auteur(proprietaire_id,auteur_id):
        return Livre.objects.all()

class Lecteur(models.Model):
    livre  = models.ForeignKey(Livre, blank = False, null = False)
    personne  = models.ForeignKey(Personne, blank = False, null = False)

    def __str__(self):
        return self.livre + ", " + self.personne


class Auteur(models.Model):
    nom    = models.CharField(max_length = 100, blank = False, null = False)
    prenom = models.CharField(max_length = 100, blank = True, null = True)

    @staticmethod
    def find_all():
        return Auteur.objects.all()

    @staticmethod
    def find_auteur(id):
        return Auteur.objects.get(pk=id)

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom


class AuteurLivre(models.Model):
    livre  = models.ForeignKey(Livre, blank = False, null = False)
    auteur  = models.ForeignKey(Auteur, blank = False, null = False)

    @staticmethod
    def find_auteur_livre(id):
        return AuteurLivre.objects.get(pk=id)
    # def __str__(self):
    #     return self.livre + ", " + self.auteur


class Location(models.Model):
    AVIS = (
        ('CHOUETTE','Chouette'),
        ('BOF','Bof'),
        ('NUL','Nul'),
        ('SUPER','Super'),
        )
    lecteur             = models.ForeignKey('Lecteur')
    livre               = models.ForeignKey('Livre')
    date_debut_location = models.DateField(auto_now = False, auto_now_add = False)
    date_fin_location   = models.DateField(auto_now = False, blank = True, null = True, auto_now_add = False)
    remarque            = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.lecteur.nom + ", " + self.livre.titre


class Proprietaire(models.Model):
    personne = models.ForeignKey(Personne)
    livre    = models.ForeignKey(Livre)

    def __str__(self):
            return self.personne.nom + ", " + self.livre.titre


    def est_disponible(self):
        print('est_disponible')
        emprunt = Emprunt.objects.filter(proprietaire = self, date_retour__isnull = True)
        if emprunt:
            print('false')
            return False
        else:
            print('true')
            return True

    def find_emprunt_by_proprietaire(proprietaire):
        print('find_emprunt_by_proprietaire')
        try:
            return Emprunt.objects.get(proprietaire = proprietaire)
        except:
            return None

    def find_emprunt_en_cours_by_proprietaire(proprietaire):
        print('find_emprunt_en_cours_by_proprietaire')
        try:
            print('try')
            return Emprunt.objects.get(proprietaire = proprietaire, date_retour__isnull=True)
        except:
            print('else')
            return None

    def emprunt_courant(self):
        print('emprunt_courant1')
        print(self)
        print(self.personne)
        emprunts =  Emprunt.objects.filter(proprietaire = self, personne=self.personne, date_retour__isnull = True)
        print('emprunt_courant2')

        for e in emprunts:
            print(e.date_retour)
        if emprunts:
            print('existe un emprunt avec date_retour = Null')
            return emprunts[0].id
        else:
            return None


class Lecture(models.Model):
    personne = models.ForeignKey(Personne,blank = False, null = False)
    livre    = models.ForeignKey(Livre, blank = False, null = False)

    def __str__(self):
            return self.personne.nom + ", " + self.livre.titre

    @staticmethod
    def find_all_by_user(user):
        print('find_all_by_user')
        person = Personne.find_personne_by_user(user)
        l= Lecture.objects.filter(personne=person)
        liste_livre=[]
        for p in l:
            print('for')
            liste_livre.append(p.livre)
        print(liste_livre)
        return liste_livre


class Emprunt(models.Model):
    personne     = models.ForeignKey(Personne,blank = False, null = False)
    proprietaire = models.ForeignKey(Proprietaire,blank = False, null = False)
    date_emprunt = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    date_retour  = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)

    @staticmethod
    def find_emprunt_courant_by_user(user):
        personne = Personne.find_personne_by_user(user)
        return Emprunt.objects.filter(personne = personne, date_retour__isnull=True)
