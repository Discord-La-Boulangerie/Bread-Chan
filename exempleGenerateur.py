liste = ["Jambon", "salami", "Vin", "Fromage",
         "couscous", "merguez", "Saucisson"]

nouvelleListe = [nom for nom in liste if not nom[0].islower()]
print(nouvelleListe)
