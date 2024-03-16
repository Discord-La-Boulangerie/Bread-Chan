from datetime import datetime, timedelta
import math

# Obtenir la date actuelle
date_actuelle = datetime.now()

# Calculer le premier jour du mois prochain
if date_actuelle.month == 12:
    premier_jour_mois_prochain = datetime(date_actuelle.year + 1, 1, 1)
else:
    premier_jour_mois_prochain = datetime(
        date_actuelle.year, date_actuelle.month + 1, 1)

# Calculer la différence en secondes
difference_en_secondes = (premier_jour_mois_prochain -
                          date_actuelle).total_seconds()
difference_en_secondes_arrondies = math.ceil(difference_en_secondes)

print("Différence en secondes (arrondies au supérieur) jusqu'au premier jour du mois prochain:",
      difference_en_secondes_arrondies)
