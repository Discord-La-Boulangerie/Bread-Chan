// Sélection du bouton du menu hamburger
const hamburgerBtn = document.querySelector('.hamburger-btn');

// Sélection de la liste de navigation
const navbarList = document.getElementById('navbarList');

// Ajout d'un écouteur d'événement au clic sur le bouton du menu hamburger
hamburgerBtn.addEventListener('click', function() {
  // Vérifier si la liste de navigation est actuellement visible
  if (navbarList.style.display === 'none' || navbarList.style.display === '') {
    // Afficher la liste de navigation
    navbarList.style.display = 'flex';
  } else {
    // Masquer la liste de navigation
    navbarList.style.display = 'none';
  }
});