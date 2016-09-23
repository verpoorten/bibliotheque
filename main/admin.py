from django.contrib import admin

from .models import  *


admin.site.register(Personne)
admin.site.register(Lecteur)
admin.site.register(Auteur, AuteurAdmin)
admin.site.register(Categorie)
admin.site.register(Livre, LivreAdmin)
admin.site.register(AuteurLivre, AuteurLivreAdmin)
admin.site.register(Location)
admin.site.register(Proprietaire, ProprietaireAdmin)
admin.site.register(Lecture)
admin.site.register(Emprunt)
