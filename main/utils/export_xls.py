from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Color, Style, PatternFill
from django.utils.translation import ugettext_lazy as _

from main.models import *


HEADER = [str(_('Titre')),
          str(_('Auteur(s)')),
          str(_('Proprietaire(s)')),
          str(_('Lu/pas lu'))]

def export_xls_livres(request):

    livres = Livre.find_all()

    wb = Workbook()
    ws = wb.active
    __columns_ajusting(ws)
    if request.user.is_authenticated():
        ws.append(HEADER)
        nom_fichier = str(request.user) + "_livres.xlsx"
    else:
        ws.append([str(_('Titre')),
                   str(_('Auteur(s)')),
                   str(_('Proprietaire(s)'))])
        nom_fichier ="livres.xlsx"



    cptr = 1
    for l in livres:
        proprietaires = l.proprietaires
        proprio = ""
        cpt=0
        for p in proprietaires:
            if cpt >0:
                proprio += ", " + p.personne.nom + " " +p.personne.prenom
            else:
                proprio +=  p.personne.nom + " " + p.personne.prenom
            cpt=cpt+1
        etat_lecture = ""

        if request.user.is_authenticated():
            lecture = Livre.find_lecture(l.id,request.user)
            if lecture:
                etat_lecture="Lu"
        auteurs = l.auteurs_livres_str
        ws.append([l.titre,
                   str(auteurs),
                   str(proprio),
                   etat_lecture])

    response = HttpResponse(content=save_virtual_workbook(wb))
    response['Content-Disposition'] = 'attachment; filename=%s' % nom_fichier
    response['Content-type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return response


def __columns_ajusting(ws):
    """
    ajustement des colonnes à la bonne dimension
    """
    col_academic_year = ws.column_dimensions['A']
    col_academic_year.width = 40
    col_academic_year = ws.column_dimensions['B']
    col_academic_year.width = 40
    col_academic_year = ws.column_dimensions['C']
    col_academic_year.width = 20
