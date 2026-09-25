// Chapter links seek the explainer video instead of navigating.
document.querySelectorAll("[data-seek]").forEach((link) => {
  link.addEventListener("click", (event) => {
    const video = document.getElementById("explainer");
    event.preventDefault();
    video.currentTime = Number(link.dataset.seek);
    video.play();
    video.scrollIntoView({ behavior: "smooth", block: "center" });
  });
});
