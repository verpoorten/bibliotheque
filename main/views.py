from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from main.models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone


def page_not_found(request):
    return render(request, 'page_not_found.html')


def access_denied(request):
    return render(request, 'acces_denied.html')


def home(request):
    if request.user.is_authenticated():
        livres = Livre.find_last_by_user(request.user)
        if livres:
            livres = livres[:10]
        lectures = Lecture.find_last_by_user(request.user)
        if lectures:
            lectures = lectures[:10]
        return render(request, 'home.html',
                      {'livres':  livres,
                       'lectures': lectures,
                       'emprunts': Emprunt.find_emprunt_courant_by_user(request.user),
                       'en_locations': Emprunt.find_locations(request.user)})
    else:
        return render(request, 'home.html', {})


def auteur_list(request):
        return render(request, 'auteur_list.html', {'auteurs': Auteur.find_all()})


def auteur_create(request):
    auteur = Auteur()
    return render(request, "auteur_form.html",
                  {'auteur':         auteur})


def auteur_form(request, auteur_id):
    auteur = Auteur.find_auteur(auteur_id)

    return render(request, "auteur_form.html",
                  {'auteur':     auteur})


def auteur_new(request):
    auteur = Auteur()

    auteur.nom = request.POST['nom']
    auteur.prenom = request.POST['prenom']

    auteur.save()


def auteur_update(request):

    auteur = Auteur()

    if ('add' == request.POST['action'] or 'modify' == request.POST['action']):
        if request.POST['id'] and not request.POST['id'] == 'None':
            auteur = get_object_or_404(Auteur, pk=request.POST['id'])
        else:
            auteur = Auteur()
        auteur.nom = request.POST['nom']
        auteur.prenom = request.POST['prenom']

        auteur.save()

    return render(request, 'auteur_list.html', {'auteurs': Auteur.find_all()})


def auteur_delete(request, id):
    auteur = get_object_or_404(Auteur, pk=id)
    auteur.delete()
    return render(request, 'auteur_list.html', {'auteurs': Auteur.find_all()})


def livre_my_list(request):
    personne = Personne.find_personne_by_user(request.user)
    livres = None
    if personne:
        livres = Livre.find_by_proprietaire(personne.id)

    return render(request, 'livre_list.html',
                  {'livres':    livres,
                   'personnes': Proprietaire.find_distinct(),
                   'auteurs':   Auteur.objects.all(),
                   'titre':     None,
                   'auteur':    None,
                   'personne':  personne.id})


def livre_search(request):
    query = Livre.objects.all()
    personne = None
    auteur = None
    livres = Livre.find_all()
    if request.GET['personne_id']:
        personne = request.GET['personne_id']
        livres = Livre.find_by_proprietaire(personne)

    if request.GET['auteur_id']:
        auteur = request.GET['auteur_id']
        livres = Livre.find_by_auteur(auteur)

    titre = None
    if request.GET['titre']:
        titre = request.GET['titre']
        livres = Livre.find_by_titre(request.GET['titre'])
    # livres = Livre.find_by_proprietaire_auteur(proprietaire, auteur)
    if request.user.is_authenticated():
        if request.GET['lu']:
            etat_lecture = request.GET['lu']
            if etat_lecture == "lu":
                livres = Livre.find_by_etat_lecture(True, request.user)
            else:
                if etat_lecture == "paslu":
                    livres = Livre.find_by_etat_lecture(False, request.user)

    personne_id = None
    if personne:
        personne_id = int(personne)

    return render(request, 'livre_list.html',
                  {'livres':    livres,
                   'personnes': Proprietaire.find_distinct(),
                   'auteurs':   Auteur.objects.all(),
                   'titre':     titre,
                   'auteur':    auteur,
                   'personne':  personne_id})


def livre_list(request):
    return render(request, 'livre_list.html',
                  {'livres': Livre.find_all(),
                   'personnes': Proprietaire.find_distinct(),
                   'auteurs': Auteur.objects.all()})


def livre_create(request):
    livre = Livre()
    return render(request, "livre_form_new.html",
                  {'livre':      livre,
                   'categories': Categorie.objects.all(),
                   'personnes':  Proprietaire.find_distinct(),
                   'auteurs':    Auteur.objects.all()})


def livre_form(request, livre_id):
    livre = Livre.find_livre(livre_id)
    lecture = None
    if request.user.is_authenticated():
        lecture = Livre.find_lecture(livre_id, request.user)

    user = None
    if request.user.is_authenticated():
        user = request.user

    return render(request, "livre_form.html",
                  {'livre':      livre,
                   'categories': Categorie.objects.all(),
                   'lecture':    lecture,
                   'user':       user})


def livre_update(request):
    livre = Livre()

    if ('add' == request.POST['action'] or 'modify' == request.POST['action']):
        if request.POST['id'] and not request.POST['id'] == 'None':
            livre = get_object_or_404(Livre, pk=request.POST['id'])
        else:
            livre = Livre()
        livre.titre = request.POST['titre']
        livre.langue = request.POST['langue']


        if request.POST['categorie'] and not request.POST['categorie'] == 'None':
            categorie = get_object_or_404(Categorie, pk=request.POST['categorie'])
        else:
            categorie = None
        livre.categorie = categorie
        livre.save()
        lu=False
        if request.POST.get('lu', None) == "on":
            lu= True
        if lu:
            lecture = Livre.find_lecture(livre.id, request.user)
            if lecture:
                pass
            else:
                personne = Personne.find_personne_by_user(request.user)
                lecture = Lecture()
                lecture.livre = livre
                lecture.personne = personne
                lecture.save()
        else:
            lecture = Livre.find_lecture(livre.id, request.user)
            if lecture:
                lecture.delete()

    return render(request, 'livre_list.html', {'livres': Livre.find_all()})


def livre_delete(request, id):
    livre = get_object_or_404(Livre, pk=id)
    livre.delete()
    return render(request, 'livre_list.html', {'livres': Livre.find_all()})


def livre_new(request):
    livre = Livre()

    livre.titre = request.POST['titre']
    livre.langue = request.POST['langue']

    if request.POST['categorie'] and not request.POST['categorie'] == 'None':
        categorie = get_object_or_404(Categorie, pk=request.POST['categorie'])
    else:
        categorie = None
    livre.categorie = categorie
    livre.save()
    lu=False
    if request.POST.get('lu', None) == "on":
        lu= True
    if lu:
        lecture = Livre.find_lecture(livre.id, request.user)
        if lecture:
            pass
        else:
            personne = Personne.find_personne_by_user(request.user)
            lecture = Lecture()
            lecture.livre  = livre
            lecture.personne = personne
            lecture.save()
    else:
        lecture = Livre.find_lecture(livre.id, request.user)
        if lecture:
            lecture.delete()
    if request.POST['auteur_id']:
        auteur = get_object_or_404(Auteur, pk=request.POST['auteur_id'])
        auteur_livre = AuteurLivre()
        auteur_livre.auteur = auteur
        auteur_livre.livre = livre
        auteur_livre.save()

    if request.POST['personne_id']:
        personne = get_object_or_404(Personne, pk=request.POST['personne_id'])
        proprietaire = Proprietaire()
        proprietaire.personne = personne
        proprietaire.livre = livre
        proprietaire.save()

    return render(request, 'livre_list.html',  {'livres': Livre.find_all()})


def delete_auteur_livre(request, auteur_livre_id):
    auteur_livre = AuteurLivre.find_auteur_livre(auteur_livre_id)
    livre = auteur_livre.livre
    auteur_livre.delete()
    return render(request, "livre_form.html",
                  {'livre': livre,
                   'categories': Categorie.objects.all()})


def add_auteur_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)
    auteur = Auteur()
    auteur.livre= livre

    return render(request, "auteur_form.html",
                  {'auteur':     auteur,
                   'categories': Categorie.objects.all()})


def add_auteur_to_livre(request, livre_id):
    livre = get_object_or_404(Livre, pk=livre_id)
    auteur_livre = AuteurLivre()
    auteur_livre.livre= livre

    return render(request, "auteur_livre_form.html",
                  {'auteur_livre': auteur_livre,
                   'auteurs':      Auteur.find_all(),
                   'livre':        livre,
                   'categories':   Categorie.objects.all()})


def save_auteur_livre(request):
    auteur_id=request.POST['auteur_id']
    livre_id=request.POST['livre_id']
    auteur_livre = AuteurLivre()
    auteur = get_object_or_404(Auteur, pk=auteur_id)
    livre = get_object_or_404(Livre, pk=livre_id)
    auteur_livre.livre = livre
    auteur_livre.auteur = auteur
    auteur_livre.save()

    return render(request, "livre_form.html",
                  {'livre': livre,
                   'categories': Categorie.objects.all()})

def add_proprietaire_to_livre(request, livre_id):
    proprietaire = Proprietaire()
    livre = get_object_or_404(Livre, pk=livre_id)
    proprietaire.livre = livre
    personnes = Personne.find_all()
    return render(request, "proprietaire_form.html",
                  {'proprietaire': proprietaire,
                   'personnes':    personnes})


def save_proprietaire(request):
    livre = get_object_or_404(Livre, pk=request.POST['livre_id'])
    proprietaire  = Proprietaire()
    proprietaire.livre = livre
    personne = get_object_or_404(Personne, pk=request.POST['personne_id'])
    proprietaire.personne = personne
    proprietaire.save()
    return render(request, "livre_form.html",
                  {'livre': livre,
                   'categories': Categorie.objects.all()})


def delete_proprietaire(request, proprietaire_id):
    proprietaire = get_object_or_404(Proprietaire, pk=proprietaire_id)
    livre = proprietaire.livre
    proprietaire.delete()
    return render(request, "livre_form.html",
                  {'livre': livre,
                   'categories': Categorie.objects.all(),})


def proprietaire_emprunt_livre(request, proprietaire_id):
    proprietaire = get_object_or_404(Proprietaire, pk=proprietaire_id)
    livre = proprietaire.livre
    emprunt = Proprietaire.find_emprunt_en_cours_by_proprietaire(proprietaire)
    if emprunt:
        pass
    else:
        emprunt = Emprunt()
        personne = Personne.find_personne_by_user(request.user)
        emprunt.personne = personne
        emprunt.proprietaire=proprietaire
        emprunt.date_emprunt=timezone.now()
        emprunt.date_retour = None
        emprunt.livre = livre
        emprunt.save()
    lecture = Livre.find_lecture(livre.id,request.user)
    return render(request, "livre_form.html",
                  {'livre':     livre,
                   'categories': Categorie.objects.all(),
                   'lecture':   lecture})

def proprietaire_retour_livre(request, emprunt_id):
    """
    Indique un livre comme rendu
    param: request
    param: emprunt_id
    """
    emprunt = get_object_or_404(Emprunt, pk=emprunt_id)

    if emprunt:
        emprunt.date_retour = timezone.now()
        emprunt.save()
    livre = get_object_or_404(Livre, pk=emprunt.proprietaire.livre.id)
    lecture = Livre.find_lecture(livre.id,request.user)

    return render(request, "livre_form.html",
                  {'livre':     livre,
                   'categories': Categorie.objects.all(),
                   'lecture':   lecture})


def lecture_retour_lu_livre(request, emprunt_id):
        """
        Indique un livre comme rendu et ajoute un enregistrement lecture
        Exécuté depuis la page home
        """
        emprunt = get_object_or_404(Emprunt, pk=emprunt_id)

        if emprunt:
            emprunt.date_retour = timezone.now()
            emprunt.save()
        livre = get_object_or_404(Livre, pk=emprunt.proprietaire.livre.id)
        lecture = Lecture.find_lecture(livre, emprunt.personne)

        if lecture:
            pass
        else:
            person = Personne.find_by_id(emprunt.personne.id)
            lecture = Lecture()
            lecture.personne = person
            lecture.livre = livre
            lecture.save()

        return home(request)


def proprietaire_retour_lu_livre(request, emprunt_id):
    """
    Indique un livre comme rendu et ajoute un enregistrement lecture
    Exécuté depuis la page home
    """
    emprunt = get_object_or_404(Emprunt, pk=emprunt_id)

    if emprunt:
        emprunt.date_retour = timezone.now()
        emprunt.save()
    livre = get_object_or_404(Livre, pk=emprunt.proprietaire.livre.id)
    lecture = Livre.find_lecture(livre.id,request.user)

    if lecture:
        pass
    else:
        person = Personne.find_personne_by_user(request.user)
        lecture = Lecture()
        lecture.personne = person
        lecture.livre = livre
        lecture.save()

    return home(request)


def sign_in_new(request):
    """
    Manage sign in view
    :param request: the http request
    :return: the sign_in view
    """
    return render(request,'sign_in_new.html',)


def sign_in(request):
    """
    Manage sign in view
    :param request: the http request
    :return: the sign_in view
    """
    return render(request,'sign_in.html',)


def do_sign_in_new(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        localite = request.POST['localite']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('home'))
            else:
                # Return a 'disabled account' error message
                return render(request,'sign_in.html',{ 'error_messages' : ('Compte inactivé',),})
        else:
            try:
                user = User.objects.get(username=username)
                return render(request,'sign_in.html',{ 'error_messages' : ('Nom d\'utilisateur déjà existant',),})
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                try:
                    user = User.objects.create_user(username, email, password)

                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    personne = Personne()
                    personne.nom=nom
                    personne.prenom=prenom
                    personne.localite=localite
                    personne.user = user
                    personne.save()
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            # Redirect to a success page.
                            return HttpResponseRedirect(reverse('home'))

                except:
                    return render(request, 'sign_in.html',
                                  {'error_messages': ('Problème lors de l\'inscription',)})

            return HttpResponseRedirect(reverse('home'))

        return render_to_response('sign_in.html',context_instance=RequestContext(request))


def do_sign_in(request):
    """
    Perform sign in with information from POST
    :param request: the http request
    :return:The main menu if the user start on the site, the page from where the user went if not.
    """
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('home'))
            else:
                # Return a 'disabled account' error message
                return render(request,'sign_in.html', {'error_messages' : ('Compte inactivé',)})
        else:
            # Return an 'invalid login' error message.
            return render(request,'sign_in.html', {'error_messages' : ('Utilisateur ou mot de pass invalide',)})
        return render_to_response('sign_in.html', context_instance=RequestContext(request))


def log_out(request):
    """
    Perform logout from session
    :param request: the httprequest
    :return: The sign_in view
    """
    logout(request)
    return render(request, 'sign_in.html', {'info_messages': ('Successfully log out',)})


def lecteur_list(request):
    return render(request, 'lecteur_list.html', {'lecteurs': Personne.find_all()})
