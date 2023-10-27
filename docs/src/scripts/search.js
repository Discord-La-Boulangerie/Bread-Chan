function searchPage() {
    var input = document.getElementById("search-input").value.toLowerCase();
    var sections = document.querySelectorAll("section");

    for (var i = 0; i < sections.length; i++) {
        var section = sections[i];
        var content = section.textContent.toLowerCase();

        if (content.includes(input)) {
            section.style.display = "block";
        } else {
            section.style.display = "none";
        }
    }
}