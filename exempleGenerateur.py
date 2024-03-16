class UnautorisedWordError(Exception):
    """Classe d'erreur pour les chaînes contenant des mots interdits."""

    def __init__(self, message="La chaîne contient des mots interdits"):
        self.message = message
        super().__init__(self.message)

# Exemple d'utilisation


def checkString(chaine):
    mots_interdits = ['interdit1', 'interdit2', 'interdit3']
    for mot in mots_interdits:
        if mot in chaine:
            raise UnautorisedWordError()


# # Utilisation
# try:
#     checkString("Ceci est une phrase avec interdit1")
# except UnautorisedWordError as e:
#     print(e)  # Affiche : La chaîne contient des mots interdits


# Chaîne d'origine
chaine = "exemple"

# Remplacer le caractère à l'index 0 par 'N'
nouvelle_chaine = 'N' + chaine[1:]

print(nouvelle_chaine)  # Affiche "Nxemple"
