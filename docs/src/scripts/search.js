document.getElementById("search-input").addEventListener("keyup", function() {
    let input, filter, sections;
    input = document.getElementById("search-input");
    filter = input.value.toUpperCase();
    sections = document.querySelectorAll("section");

    for (let i = 0; i < sections.length; i++) {
        let section = sections[i];
        let content = section.textContent.toUpperCase(); // Utilisez toUpperCase ici pour faire correspondre la casse

        if (content.includes(filter)) { // Utilisez le filtre plutôt que l'input
            section.style.display = "";
        } else {
            section.style.display = "none";
        }
    }
});