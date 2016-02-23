from django.contrib import admin

from .models import Personne
from .models import Lecteur
from .models import Auteur
from .models import Livre
from .models import Location
from .models import Proprietaire
from .models import AuteurLivre

admin.site.register(Personne)
admin.site.register(Lecteur)
admin.site.register(Auteur)
admin.site.register(Livre)
admin.site.register(AuteurLivre)
admin.site.register(Location)
admin.site.register(Proprietaire)
