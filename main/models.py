from django.db import models

class Lecteur(models.Model):
    nom    = models.CharField(max_length = 100)
    prenom = models.CharField(max_length = 100)
    def __str__(self):
        return self.nom.upper() + ", " + self.prenom


class Auteur(models.Model):
    nom    = models.CharField(max_length = 100)
    prenom = models.CharField(max_length = 100, blank = True, null = True)

    @staticmethod
    def find_all():
        return Auteur.objects.all()

    @staticmethod
    def find_auteur(id):
        return Auteur.objects.get(pk=id)

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom


class Livre(models.Model):
    LANGUE = (
        ('FR','Français'),
        ('ENG','Anglais')
    )
    titre  = models.CharField(max_length = 100)
    langue    = models.CharField(max_length=5,choices = LANGUE, default = 'FR')

    def __str__(self):
        return self.titre


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
    proprietaire = models.ForeignKey('Lecteur')
    livre        = models.ForeignKey('Livre')

def __str__(self):
        return self.proprietaire.nom + ", " + self.livre.titre
