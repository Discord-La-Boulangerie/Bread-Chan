import re

phrase = "Bonjour, j'aime la bite, et j'habite à ma maison."

# Utilisation d'une expression régulière pour rechercher le mot "je" en tant que mot distinct
mot_a_chercher = "bite"
expression_reguliere = fr"\b{re.escape(mot_a_chercher)}\b"

if re.search(expression_reguliere, phrase, re.IGNORECASE):
    print(f"Le mot '{mot_a_chercher}' a été trouvé dans la phrase.")
else:
    print(f"Le mot '{mot_a_chercher}' n'a pas été trouvé dans la phrase.")
