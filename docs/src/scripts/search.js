document.getElementById("search-input").addEventListener("keyup", function() { // vérifie si l'utilisateur écrit dans l'élément search-input
    let input, filter, sections; // déclaration des variables
    input = document.getElementById("search-input"); // récupère les infos de la search-input
    filter = input.value.toUpperCase(); // convertit l'input en majuscules
    sections = document.querySelectorAll("section"); // récupère les infos de la section

    for (let i = 0; i < sections.length; i++) { // j'en sais rien
        let section = sections[i]; // pareil
        let content = section.textContent.toUpperCase(); // Utiliser toUpperCase ici pour faire correspondre la casse avec le filtre

        if (content.includes(filter)) { // Utiliser le filtre
            section.style.display = ""; // ne modifie pas l'affichage des sections 
        } else {
            section.style.display = "none"; // désactive l'affichage des sections ne correspondant pas avec la recherche
        }
    }
});