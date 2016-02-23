from django.db import models

class Personne(models.Model):
    nom    = models.CharField(max_length = 100, blank = False, null = False)
    prenom = models.CharField(max_length = 100, blank = False, null = False)

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom

class Livre(models.Model):
    LANGUE = (
        ('FR','Français'),
        ('ENG','Anglais')
    )
    titre  = models.CharField(max_length = 100, blank = False, null = False)
    langue    = models.CharField(max_length=5,choices = LANGUE, default = 'FR')

    @staticmethod
    def find_all():
        return Livre.objects.all()

    @staticmethod
    def find_livre(id):
        return Livre.objects.get(pk=id)

    def auteurs_livres(self):
        return AuteurLivre.objects.filter(livre=self)

    def __str__(self):
        return self.titre

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
    livre        = models.ForeignKey(Livre)

def __str__(self):
        return self.personne.nom + ", " + self.livre.titre
