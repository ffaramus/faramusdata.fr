// Figure 1 : passage d'un exemple à l'autre (images et mesures), toutes les 5 secondes.
// Choisir un exemple arrête le défilement ; le bouton le met en pause ou le relance (critère WCAG 2.2.2).
// Rien ne défile si le visiteur a demandé à limiter les animations. Sans JavaScript, le premier
// exemple reste affiché et les commandes restent masquées.

const DELAI = 5000;

document.querySelectorAll(".figure").forEach((figure) => {
  const commandes = figure.querySelector(".figure-commandes");
  const boutons = [...figure.querySelectorAll(".exemple")];
  const lecture = figure.querySelector(".figure-lecture");
  if (!commandes || boutons.length === 0 || !lecture) return;

  const images = figure.querySelectorAll("[data-panneau]");
  const mesures = figure.querySelectorAll("[data-mesure]");
  // dossier des panneaux, déduit de l'image affichée : marche depuis n'importe quelle page
  const dossier = images[0].getAttribute("src").replace(/[^/]*$/, "");
  const chemin = (bouton, img) => `${dossier}${bouton.dataset.cle}-${img.dataset.panneau}.webp`;
  let courant = 0;
  let minuteur = null;

  const precharger = (bouton) => {
    images.forEach((img) => {
      new Image().src = chemin(bouton, img);
    });
  };

  const afficher = (index) => {
    courant = index;
    const bouton = boutons[index];
    images.forEach((img) => {
      img.src = chemin(bouton, img);
      img.width = bouton.dataset.largeur;
      img.height = bouton.dataset.hauteur;
      img.alt = bouton.dataset[img.dataset.panneau];
    });
    mesures.forEach((dd) => {
      dd.textContent = bouton.dataset[dd.dataset.mesure];
    });
    boutons.forEach((b, i) => b.setAttribute("aria-pressed", String(i === index)));
    precharger(boutons[(index + 1) % boutons.length]);
  };

  const majLecture = () => {
    lecture.textContent = minuteur ? "Mettre en pause" : "Lancer le défilement";
  };

  const demarrer = () => {
    clearInterval(minuteur);
    minuteur = setInterval(() => afficher((courant + 1) % boutons.length), DELAI);
    majLecture();
  };

  const arreter = () => {
    clearInterval(minuteur);
    minuteur = null;
    majLecture();
  };

  boutons.forEach((bouton, i) => {
    bouton.addEventListener("click", () => {
      arreter();
      afficher(i);
    });
  });
  lecture.addEventListener("click", () => (minuteur ? arreter() : demarrer()));

  commandes.hidden = false;
  precharger(boutons[1 % boutons.length]);
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    arreter();
  } else {
    demarrer();
  }
});
