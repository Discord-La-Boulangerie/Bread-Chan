function searchPage() {
    var input = document.getElementById("search-input").value.toLowerCase();
    var sections = document.querySelectorAll("section");
    var noResultsMessages = document.querySelectorAll(".no-results-message");

    var foundResults = false;

    for (var i = 0; i < sections.length; i++) {
        var section = sections[i];
        var content = section.textContent.toLowerCase();

        if (content.includes(input)) {
            section.style.display = "block";
            foundResults = true;
        } else {
            section.style.display = "none";
        }
    }

    for (var i = 0; i < noResultsMessages.length; i++) {
        if (foundResults) {
            noResultsMessages[i].style.display = "none";
        } else {
            noResultsMessages[i].style.display = "block";
        }
    }
}