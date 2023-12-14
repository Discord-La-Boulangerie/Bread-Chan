document.getElementById("searchInput").addEventListener("keyup", function () {
    let input, filter, sections;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    sections = document.querySelectorAll("section");

    for (var i = 0; i < sections.length; i++) {
        var section = sections[i];
        var content = section.textContent.toUpperCase(); // Utilisez toUpperCase ici pour faire correspondre la casse

        if (content.includes(filter)) { // Utilisez le filtre plutôt que l'input
            section.style.display = "block";
        } else {
            section.style.display = "none";
        }
    }
});