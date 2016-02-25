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

class Livre(models.Model):
    LANGUE = (
        ('FR','Français'),
        ('ENG','Anglais')
    )
    titre  = models.CharField(max_length = 100, blank = False, null = False)
    langue    = models.CharField(max_length=5,choices = LANGUE, default = 'FR')


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
