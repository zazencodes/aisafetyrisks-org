// Chapter links seek the explainer video instead of navigating; a #t=<seconds> URL opens at that time.
const video = document.getElementById("explainer");

document.querySelectorAll("[data-seek]").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    video.currentTime = Number(link.dataset.seek);
    video.play();
    video.scrollIntoView({ behavior: "smooth", block: "center" });
  });
});

const start = location.hash.match(/^#t=(\d+)$/);
if (start) {
  video.currentTime = Number(start[1]);
  video.scrollIntoView({ block: "center" });
}
