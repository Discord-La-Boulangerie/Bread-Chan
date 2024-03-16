liste = ["Jambon", "salami", "Vin", "Fromage",
         "couscous", "merguez", "Saucisson"]

nouvelleListe = []
for i in range(len(liste)):
    if not liste[i].islower():
        nouvelleListe.append(liste[i])


print(nouvelleListe)
