// Vidéos des figures : lecture sans son et en boucle, sauf si le visiteur a demandé
// à limiter les animations. Un bouton permet de mettre en pause (critère WCAG 2.2.2).
// Sans JavaScript, la vidéo garde ses commandes natives et n'est pas lancée.

document.querySelectorAll(".figure-video").forEach((video) => {
  const bouton = video.closest("figure")?.querySelector(".figure-lecture");
  if (!bouton) return;

  video.removeAttribute("controls");
  bouton.hidden = false;

  const majBouton = () => {
    bouton.textContent = video.paused ? "Lire la vidéo" : "Mettre en pause";
  };
  video.addEventListener("play", majBouton);
  video.addEventListener("pause", majBouton);
  bouton.addEventListener("click", () => {
    if (video.paused) {
      video.play();
    } else {
      video.pause();
    }
  });

  const animationsReduites = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!animationsReduites) {
    video.play().catch(() => {});
  }
  majBouton();
});
