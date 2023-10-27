function searchPage() {
    var input = document.getElementById("search-input").value.toLowerCase();
    var sections = document.querySelectorAll("section");
    var noResultsMessage = document.getElementById("no-results-message");

    var foundResults = false; // Pour suivre si des résultats ont été trouvés

    for (var i = 0; i < sections.length; i++) {
        var section = sections[i];
        var content = section.textContent.toLowerCase();

        if (content.includes(input)) {
            section.style.display = "block";
            foundResults = true; // Au moins un résultat a été trouvé
        } else {
            section.style.display = "none";
        }
    }

    if (!foundResults) {
        // Aucun résultat trouvé, afficher un message d'erreur
        noResultsMessage.style.display = "block";
    } else {
        // Des résultats ont été trouvés, masquer le message d'erreur
        noResultsMessage.style.display = "none";
    }
}