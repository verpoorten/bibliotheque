from django.contrib import admin

from .models import Personne
from .models import Lecteur
from .models import Auteur
from .models import Categorie
from .models import Livre
from .models import Location
from .models import Proprietaire
from .models import AuteurLivre
from .models import Lecture
from .models import Emprunt


admin.site.register(Personne)
admin.site.register(Lecteur)
admin.site.register(Auteur)
admin.site.register(Categorie)

class LivreAdmin(admin.ModelAdmin):
    search_fields = ['titre']

admin.site.register(Livre,LivreAdmin)

class AuteurLivreAdmin(admin.ModelAdmin):
    raw_id_fields = ('livre', 'auteur' )

admin.site.register(AuteurLivre, AuteurLivreAdmin)

admin.site.register(Location)
class ProprietaireAdmin(admin.ModelAdmin):
    raw_id_fields = ('personne', 'livre' )

admin.site.register(Proprietaire, ProprietaireAdmin)
admin.site.register(Lecture)
admin.site.register(Emprunt)
