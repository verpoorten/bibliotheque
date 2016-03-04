from django.db import models
from django.contrib.auth.models import User

class Personne(models.Model):
    nom    =   models.CharField(max_length = 50, blank = False, null = False)
    prenom =   models.CharField(max_length = 50, blank = False, null = False)
    localite = models.CharField(max_length = 50, blank = True, null = True)
    user   =   models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nom.upper() + ", " + self.prenom

    def find_all():
        return Personne.objects.all()

    def find_all_exclude_user(current_user):
        return Personne.objects.all().exclude(user = current_user)

    @staticmethod
    def find_personne_by_user(user):
        try:
            return Personne.objects.get(user=user)
        except:
            return None

    @staticmethod
    def find_by_id(id):
        return Personne.objects.get(pk=id)

class Categorie(models.Model):
    libelle = models.CharField(max_length = 100, blank = False, null = False)

    def __str__(self):
        return self.libelle


class Livre(models.Model):
    LANGUE = (
        ('FR','Français'),
        ('ENG','Anglais')
    )

    titre             = models.CharField(max_length = 100, blank = False, null = False)
    langue            = models.CharField(max_length=5,choices = LANGUE, default = 'FR')
    categorie         = models.ForeignKey(Categorie, blank = True, null = True)
    date_creation     = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    date_modification = models.DateTimeField(auto_now=True, blank = True, null = True)

    @property
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
    def find_last_by_user(user):
        liste_livre=[]
        if  user.is_authenticated():
            person = Personne.find_personne_by_user(user)
            l= Proprietaire.objects.filter(personne=person).order_by('-livre__date_modification')

            for p in l:
                liste_livre.append(p.livre)

        return liste_livre

    @staticmethod
    def find_all_by_user(user):
        liste_livre=[]
        if  user.is_authenticated():
            person = Personne.find_personne_by_user(user)

            l= Proprietaire.objects.filter(personne=person)

            for p in l:
                liste_livre.append(p.livre)

        return liste_livre
    @staticmethod
    def find_all_lecture_by_user(user):
        liste_livre=[]
        if  user.is_authenticated():
            person = Personne.find_personne_by_user(user)
            l= Lecture.objects.filter(personne=person)
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
    @property
    def auteurs_livres_str(self):
        s = ""
        cpt=0
        for al in  AuteurLivre.objects.filter(livre=self):
            if cpt>0:
                s = s + ", " + str(al.auteur)
            else:
                s = al.auteur
            cpt=cpt+1
        return s

    @staticmethod
    def find_by_proprietaire_auteur(proprietaire_id,auteur_id):
        return Livre.objects.all()

    @staticmethod
    def find_by_proprietaire(personne_id):
        personne = None
        if personne_id:
            personne = Personne.find_by_id(personne_id)

        livres=[]
        if personne:
            #proprietaire
            list_proprietaire =Proprietaire.objects.filter(personne = personne)
            for l in list_proprietaire:
                livres.append(l.livre)

        return livres
    @staticmethod
    def find_by_auteur(auteur_id):

        auteur = None
        if auteur_id:
            auteur = Auteur.find_auteur(auteur_id)
        livres=[]

        if auteur:
            list_livre_auteur = AuteurLivre.objects.filter(auteur=auteur)
            for l in list_livre_auteur:
                livres.append(l.livre)
        return livres

    @staticmethod
    def find_by_titre(titre):
        return Livre.objects.filter(titre__icontains = titre)

class Lecteur(models.Model):
    livre  = models.ForeignKey(Livre, blank = False, null = False)
    personne  = models.ForeignKey(Personne, blank = False, null = False)

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

        q= Lecteur.objects.values('personne').distinct()
        #[{'personne': 3}, {'personne': 8}]
        personnes = []
        for engt in q:
            print(engt.get('personne'))
            p=Personne.find_by_id(engt.get('personne'))
            print (p)
            if p :
                print('if')
                personnes.append(p)

        return personnes

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
    @staticmethod
    def find_auteur_livre_by_auteur(auteur):
        return AuteurLivre.objects.filter(auteur=auteur)
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
        emprunt = Emprunt.objects.filter(proprietaire = self, date_retour__isnull = True)
        if emprunt:
            return False
        else:
            return True
    @staticmethod
    def find_emprunt_by_proprietaire(proprietaire):
        try:
            return Emprunt.objects.get(proprietaire = proprietaire)
        except:
            return None
    @staticmethod
    def find_emprunt_en_cours_by_proprietaire(proprietaire):
        try:

            return Emprunt.objects.get(proprietaire = proprietaire, date_retour__isnull=True)
        except:
            return None

    def emprunt_courant(self):
        emprunts =  Emprunt.objects.filter(proprietaire = self, personne=self.personne, date_retour__isnull = True)

        if emprunts:
            print('existe un emprunt avec date_retour = Null')
            return emprunts[0].id
        else:
            return None

    @staticmethod
    def find_by_personne(personne):
        return Proprietaire.objects.filter(personne=personne)

    @staticmethod
    def find_distinct():
        print('find_distinct')
        q= Proprietaire.objects.values('personne').distinct()
        #[{'personne': 3}, {'personne': 8}]
        personnes = []
        print (q)
        for engt in q:
            print(engt.get('personne'))
            p=Personne.find_by_id(engt.get('personne'))
            print (p)
            if p :
                print('if')
                personnes.append(p)

        return personnes

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]


class Lecture(models.Model):
    personne          = models.ForeignKey(Personne,blank = False, null = False)
    livre             = models.ForeignKey(Livre, blank = False, null = False)
    date_creation     = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    date_modification = models.DateTimeField(auto_now=True, blank = True, null = True)

    def __str__(self):
            return self.personne.nom + ", " + self.livre.titre
    @staticmethod
    def find_by_id(id):
        return Livre.objects.get(pk=id)
    @staticmethod
    def find_all():
        return Lecture.objects.all()

    @staticmethod
    def find_last_by_user(user):
        person = Personne.find_personne_by_user(user)
        l= Lecture.objects.filter(personne=person).order_by('-livre__date_modification')
        liste_livre=[]
        for p in l:
            liste_livre.append(p.livre)
        return liste_livre

    @staticmethod
    def find_all_by_user(user):
        person = Personne.find_personne_by_user(user)
        l= Lecture.objects.filter(personne=person)
        liste_livre=[]
        for p in l:
            liste_livre.append(p.livre)
        return liste_livre

    @staticmethod
    def find_distinct():
        q= Lecture.objects.values('personne').distinct()
        personnes = []
        for engt in q:
            p=Personne.find_by_id(engt.get('personne'))
            if p :
                personnes.append(p)
        return personnes

    @staticmethod
    def find_all_by_user_livre(livre,user):
        person = Personne.find_personne_by_user(user)
        return Lecture.objects.filter(personne=person)

    def find_lecture(livre,personne):

        try:
            return Lecture.objects.get(personne=person,livre= livre)
        except:
            return None
class Emprunt(models.Model):
    personne     = models.ForeignKey(Personne,blank = False, null = False)
    proprietaire = models.ForeignKey(Proprietaire,blank = False, null = False)
    date_emprunt = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    date_retour  = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)

    @staticmethod
    def find_emprunt_courant_by_user(user):
        personne = Personne.find_personne_by_user(user)
        return Emprunt.objects.filter(personne = personne, date_retour__isnull=True)

    @staticmethod
    def find_locations(user):
        personne = Personne.find_personne_by_user(user)
        list_propriete = Proprietaire.find_by_personne(personne)
        locations = []
        for p in list_propriete:
            loc =  Emprunt.objects.filter(proprietaire = p, date_retour__isnull=True)
            for l in loc:
                locations.append(l)
        return locations
