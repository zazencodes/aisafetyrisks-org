/* Each diagram loops while visible. Scroll changes playback, not the reader's pace. */
const DURATION = 7200;
const BEATS = [0, 2400, 4800];
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

function holdThenMove(from, to, start, length = 750) {
  return [
    { ...from, offset: 0 },
    { ...from, offset: start / DURATION, easing: "cubic-bezier(0.16, 1, 0.3, 1)" },
    { ...to, offset: (start + length) / DURATION },
    { ...to, offset: 1 },
  ];
}

function makeScene(figure) {
  const stage = figure.querySelector(".scene-stage");
  const controls = figure.querySelector(".scene-controls");
  const pauseButton = figure.querySelector("[data-pause]");
  const replayButton = figure.querySelector("[data-replay]");
  const steps = [...figure.querySelectorAll(".scene-steps li")];
  const colors = getComputedStyle(figure);
  const animations = [];
  const clock = stage.animate([{}, {}], { duration: DURATION, fill: "both" });
  clock.pause();
  clock.currentTime = 0;
  let started = false;
  let completed = false;
  let inView = false;
  let userPaused = false;
  let frame = null;

  function animate(element, keyframes) {
    const animation = element.animate(keyframes, { duration: DURATION, fill: "both" });
    animation.pause();
    animation.currentTime = 0;
    animations.push(animation);
  }

  for (const element of stage.querySelectorAll("[data-motion]")) {
    const start = BEATS[Number(element.dataset.beat) - 1] + 180;
    switch (element.dataset.motion) {
      case "draw": {
        const paths = element.matches("path") ? [element] : element.querySelectorAll("path");
        for (const path of paths) {
          const length = path.getTotalLength();
          path.style.strokeDasharray = `${length}`;
          animate(path, holdThenMove({ strokeDashoffset: length }, { strokeDashoffset: 0 }, start, 1150));
        }
        break;
      }
      case "reveal":
        animate(element, holdThenMove(
          { opacity: 0, transform: "translateY(8px)" },
          { opacity: 1, transform: "translateY(0)" }, start,
        ));
        break;
      case "fade":
        animate(element, holdThenMove({ opacity: 1 }, { opacity: 0.18 }, start, 1100));
        break;
      case "lower":
        animate(element, holdThenMove({ transform: "translateY(-125px)" }, { transform: "translateY(0)" }, start, 1300));
        break;
      case "tint":
        animate(element, holdThenMove(
          { fill: colors.getPropertyValue("--paper").trim(), stroke: colors.getPropertyValue("--rule").trim() },
          { fill: colors.getPropertyValue("--accent-soft").trim(), stroke: colors.getPropertyValue("--accent").trim() }, start, 1300,
        ));
        break;
      case "orbit":
        animate(element, [
          { opacity: 0, transform: "rotate(0deg)", offset: 0 },
          { opacity: 0, transform: "rotate(0deg)", offset: start / DURATION },
          { opacity: 1, transform: "rotate(45deg)", offset: (start + 450) / DURATION, easing: "ease-in" },
          { opacity: 1, transform: "rotate(720deg)", offset: 1 },
        ]);
        break;
      case "evaluate":
        animate(element, holdThenMove({ transform: "translateX(-90px)" }, { transform: "translateX(0)" }, start, 1900));
        break;
      default:
        throw new Error(`Unknown scene motion: ${element.dataset.motion}`);
    }
  }

  function render() {
    const time = Number(clock.currentTime);
    const active = Math.min(2, Math.floor(time / 2400));
    steps.forEach((step, index) => {
      step.classList.toggle("is-current", started && index === active);
      step.classList.toggle("is-past", started && index < active);
    });
    figure.dataset.state = completed ? "complete" : clock.playState;
  }

  function tick() {
    render();
    frame = clock.playState === "running" ? requestAnimationFrame(tick) : null;
  }

  function sync() {
    if (frame !== null) cancelAnimationFrame(frame);
    frame = null;
    const running = started && !completed && inView && !userPaused && !document.hidden && !reducedMotion.matches;
    for (const animation of [clock, ...animations]) {
      if (completed) continue;
      if (running) animation.play();
      else animation.pause();
    }
    pauseButton.disabled = !started || completed;
    pauseButton.textContent = userPaused ? "Resume" : "Pause";
    pauseButton.setAttribute("aria-label", `${userPaused ? "Resume" : "Pause"} ${figure.dataset.scene} animation`);
    render();
    if (running) frame = requestAnimationFrame(tick);
  }

  function finish() {
    completed = true;
    started = true;
    for (const animation of [clock, ...animations]) animation.finish();
    sync();
  }

  function restart() {
    completed = false;
    started = true;
    userPaused = false;
    for (const animation of [clock, ...animations]) {
      animation.pause();
      animation.currentTime = 0;
    }
    sync();
  }

  clock.onfinish = () => {
    if (!reducedMotion.matches) restart();
  };

  pauseButton.addEventListener("click", () => {
    userPaused = !userPaused;
    sync();
  });
  replayButton.addEventListener("click", restart);

  function applyMotionPreference() {
    controls.hidden = reducedMotion.matches;
    if (reducedMotion.matches) finish();
    else if (completed) restart();
    else sync();
  }

  applyMotionPreference();
  return {
    stage,
    sync,
    applyMotionPreference,
    visibility(visible) {
      inView = visible;
      if (visible) started = true;
      sync();
    },
  };
}

const scenes = [...document.querySelectorAll(".story-scene")].map(makeScene);
const byStage = new Map(scenes.map(scene => [scene.stage, scene]));
const observer = new IntersectionObserver(entries => {
  for (const entry of entries) {
    byStage.get(entry.target).visibility(entry.isIntersecting && entry.intersectionRatio >= 0.45);
  }
}, { threshold: [0, 0.45] });
for (const scene of scenes) observer.observe(scene.stage);
document.addEventListener("visibilitychange", () => scenes.forEach(scene => scene.sync()));
reducedMotion.addEventListener("change", () => scenes.forEach(scene => scene.applyMotionPreference()));
