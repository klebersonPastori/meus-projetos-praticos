/* =========================================================
   Howkins RUNNER — 8bit (DOM + CSS animations)
========================================================= */
// -----------------------------
// Seletores de elementos
// -----------------------------
const $game = document.getElementById("game");
const $startHint = document.getElementById("startHint");
const $mike = document.getElementById("mikeWrap");
const $score = document.getElementById("score");
const $overlay = document.getElementById("overlay");
const $retry = document.getElementById("retry");
const $bgm = document.getElementById("bgm");

// -----------------------------
// Métricas dinâmicas
// -----------------------------
let GAME_HEIGHT = 360;
let PLAYER_HEIGHT = 48;
let MAX_Y = GAME_HEIGHT - PLAYER_HEIGHT;

function recalcSceneMetrics() {
  const gameRect = $game?.getBoundingClientRect();
  const mikeRect = $mike?.getBoundingClientRect();
  if (gameRect) GAME_HEIGHT = gameRect.height;
  if (mikeRect) PLAYER_HEIGHT = mikeRect.height;
  MAX_Y = Math.max(0, GAME_HEIGHT - PLAYER_HEIGHT);
}
window.addEventListener("load", recalcSceneMetrics);
window.addEventListener("resize", recalcSceneMetrics);

// -------- CINZAS ANIMADAS NO FUNDO --------
const ashesContainer = document.querySelector(".ashes");
function createAsh() {
  if (!ashesContainer) return;

  const ash = document.createElement("span");
  const size = Math.random() * 3 + 2;
  const left = Math.random() * window.innerWidth;
  const duration = Math.random() * 4 + 4;
  const delay = Math.random() * 4;

  ash.style.width = size + "px";
  ash.style.height = size + "px";
  ash.style.left = left + "px";
  ash.style.animationDuration = duration + "s";
  ash.style.animationDelay = delay + "s";

  ashesContainer.appendChild(ash);
  setTimeout(() => ash.remove(), (duration + delay) * 1000);
}
setInterval(createAsh, 130);

// -------- Raios --------
const fxLayer = document.querySelector(".fx-layer");

function triggerLightning() {
  if (!fxLayer) return;

  const x = Math.floor(Math.random() * 80) + 10;
  const y = Math.floor(Math.random() * 35) + 5;

  const wrapper = document.createElement("div");
  wrapper.className = "lightning-flash";

  const glow = document.createElement("div");
  glow.className = "lightning-glow";
  glow.style.setProperty("--x", `${x}%`);
  glow.style.setProperty("--y", `${y}%`);

  const svgNS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("viewBox", "0 0 100 100");
  svg.setAttribute("preserveAspectRatio", "none");
  svg.style.position = "absolute";
  svg.style.inset = "0";

  const defs = document.createElementNS(svgNS, "defs");
  const filter = document.createElementNS(svgNS, "filter");
  filter.setAttribute("id", "glow");
  const gauss1 = document.createElementNS(svgNS, "feGaussianBlur");
  gauss1.setAttribute("stdDeviation", "1.5");
  gauss1.setAttribute("result", "blur1");
  const merge = document.createElementNS(svgNS, "feMerge");
  const m1 = document.createElementNS(svgNS, "feMergeNode");
  m1.setAttribute("in", "blur1");
  const m2 = document.createElementNS(svgNS, "feMergeNode");
  m2.setAttribute("in", "SourceGraphic");
  merge.appendChild(m1);
  merge.appendChild(m2);
  filter.appendChild(gauss1);
  filter.appendChild(merge);
  defs.appendChild(filter);
  svg.appendChild(defs);

  const createBolt = (originX, originY) => {
    const segments = Math.floor(Math.random() * 3) + 4;
    let xPos = originX;
    let yPos = originY;
    const points = [`${xPos},${yPos}`];

    for (let i = 0; i < segments; i++) {
      yPos += Math.random() * 18 + 8;
      xPos += (Math.random() - 0.5) * 16;
      points.push(`${Math.max(0, Math.min(100, xPos))},${Math.min(100, yPos)}`);
    }

    const polyline = document.createElementNS(svgNS, "polyline");
    polyline.setAttribute("points", points.join(" "));
    polyline.setAttribute("fill", "none");
    polyline.setAttribute("stroke", "rgba(255, 40, 40, 0.95)");
    polyline.setAttribute("stroke-width", (Math.random() * 0.7 + 0.9));
    polyline.setAttribute("stroke-linecap", "round");
    polyline.setAttribute("stroke-linejoin", "round");
    polyline.setAttribute("filter", "url(#glow)");

    const core = document.createElementNS(svgNS, "polyline");
    core.setAttribute("points", points.join(" "));
    core.setAttribute("stroke", "rgba(255, 120, 120, 0.9)");
    core.setAttribute("stroke-width", "0.6");
    core.setAttribute("stroke-linecap", "round");
    core.setAttribute("stroke-linejoin", "round");
    core.setAttribute("fill", "none");
    core.setAttribute("filter", "url(#glow)");

    svg.appendChild(polyline);
    svg.appendChild(core);
  };

  const bolts = Math.floor(Math.random() * 3) + 1;
  for (let i = 0; i < bolts; i++) {
    const ox = x + (Math.random() - 0.5) * 8;
    const oy = y + (Math.random() - 0.5) * 6;
    createBolt(ox, oy);
  }

  wrapper.appendChild(svg);
  fxLayer.appendChild(wrapper);
  fxLayer.appendChild(glow);

  setTimeout(() => {
    wrapper.remove();
    glow.remove();
  }, 650);
}

function scheduleLightning() {
  setInterval(() => {
    triggerLightning();
  }, 2000 + Math.floor(Math.random() * 600) - 300);
}
window.addEventListener("load", scheduleLightning);

// -----------------------------
// CONFIGURAÇÃO MAIS FÁCIL
// -----------------------------
const CONFIG = {
  SCORE_PER_SEC: 60,

  // INÍCIO FÁCIL
  SPAWN_MIN_MS: 1600,
  SPAWN_MAX_MS: 2000,

  MONSTER_ANIM_MIN_S: 4.2,
  MONSTER_ANIM_MAX_S: 6.2,

  COLLISION_INSET: 14,

  JUMP_LOCK_MS: 750,
  gravity: 1800,
  jumpForce: 900,
  jumpHoldTime: 200
};

// -----------------------------
// Dificuldade Dinâmica — começa aos 10s
// -----------------------------
const DIFF = {
  START_AFTER_S: 10,       
  RAMP_DURATION_S: 45,

  SPAWN_FLOOR_MIN_MS: 800,
  SPAWN_FLOOR_MAX_MS: 1100,

  ANIM_FLOOR_MIN_S: 2.6,
  ANIM_FLOOR_MAX_S: 3.8,

  INSET_FLOOR: 10
};

const clamp01 = t => Math.max(0, Math.min(1, t));
const lerp = (a, b, t) => a + (b - a) * t;

// Easing mais suave
const easeInOutCubic = t =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

function getDifficultyParams(elapsedS) {
  const sinceStart = Math.max(0, elapsedS - DIFF.START_AFTER_S);
  const t = easeInOutCubic(clamp01(sinceStart / DIFF.RAMP_DURATION_S));

  const spawnMin = lerp(CONFIG.SPAWN_MIN_MS, DIFF.SPAWN_FLOOR_MIN_MS, t);
  const spawnMax = lerp(CONFIG.SPAWN_MAX_MS, DIFF.SPAWN_FLOOR_MAX_MS, t);

  const animMin = lerp(CONFIG.MONSTER_ANIM_MIN_S, DIFF.ANIM_FLOOR_MIN_S, t);
  const animMax = lerp(CONFIG.MONSTER_ANIM_MAX_S, DIFF.ANIM_FLOOR_MAX_S, t);

  const inset = Math.round(lerp(CONFIG.COLLISION_INSET, DIFF.INSET_FLOOR, t));

  const safeSpawnMin = Math.min(spawnMin, spawnMax - 50);

  return {
    spawn: { min: safeSpawnMin, max: spawnMax },
    monsterAnim: {
      min: Math.max(1.8, animMin),
      max: Math.max(2.0, animMax)
    },
    collisionInset: Math.max(8, inset),
    t
  };
}

// -----------------------------
// Resto do jogo (loop, spawn, hitbox…)
// -----------------------------
const MONSTERS = ["💀", "👻", "🕷️", "🧟", "👹"];

const monsterBaseOffset = emoji => {
  switch (emoji) {
    case "🕷️": return 0;
    case "🧟": return 0;
    case "💀": return 6;
    case "👹": return 14;
    case "👻": return 26;
    default: return 0;
  }
};

const STATE = { IDLE: "IDLE", RUNNING: "RUNNING", GAME_OVER: "GAME_OVER" };

const state = {
  phase: STATE.IDLE,
  startedOnce: false,
  score: 0,
  lastTime: 0,
  elapsedS: 0,
  spawnTimer: 0,
  nextSpawnDelay: 0,
  jumping: false,
  rafId: null,
  player: {
    y: 0,
    vy: 0,
    onGround: true,
    jumping: false,
    hold: false,
    holdTimer: 0
  }
};

const rand = (min, max) => Math.random() * (max - min) + min;

function scheduleNextSpawn() {
  const diff = getDifficultyParams(state.elapsedS);
  state.nextSpawnDelay = rand(diff.spawn.min, diff.spawn.max);
  state.spawnTimer = 0;
}

const getMonsters = () => document.querySelectorAll(".monster");

function isHit(a, b, inset = 0) {
  return !(
    b.left > a.right - inset ||
    b.right < a.left + inset ||
    b.top > a.bottom - inset ||
    b.bottom < a.top + inset
  );
}

function startGame() {
  if (state.phase === STATE.RUNNING) return;

  if (!state.startedOnce) state.startedOnce = true;

  $startHint.classList.add("hidden");
  $overlay.classList.remove("show");
  clearMonsters();

  state.phase = STATE.RUNNING;
  state.score = 0;
  state.lastTime = performance.now();
  state.elapsedS = 0;
  state.spawnTimer = 0;

  state.player.y = 0;
  state.player.vy = 0;
  state.player.onGround = true;
  state.player.hold = false;
  state.player.holdTimer = 0;

  scheduleNextSpawn();
  updateScoreUI();

  $bgm.volume = 0.6;
  $bgm.play().catch(() => {});

  $game.focus();
  state.rafId = requestAnimationFrame(gameLoop);
}

function gameOver() {
  if (state.phase !== STATE.RUNNING) return;

  state.phase = STATE.GAME_OVER;
  cancelAnimationFrame(state.rafId);
  state.rafId = null;

  $bgm.pause();
  $overlay.classList.add("show");
}

function clearMonsters() {
  getMonsters().forEach(m => m.remove());
}

function updateScoreUI() {
  $score.textContent = "SCORE: " + Math.floor(state.score);
}

function renderPlayer() {
  $mike.style.bottom = `${state.player.y}px`;
}

function gameLoop(now) {
  if (state.phase !== STATE.RUNNING) return;

  const dt = Math.min(0.032, (now - state.lastTime) / 1000);
  state.lastTime = now;
  state.elapsedS += dt;

  // física do player
  if (!state.player.onGround) {
    if (state.player.hold) {
      state.player.holdTimer -= dt * 1000;
      if (state.player.holdTimer <= 0) state.player.hold = false;
    } else {
      state.player.vy -= CONFIG.gravity * dt;
    }

    state.player.y += state.player.vy * dt;

    if (state.player.y >= MAX_Y) {
      state.player.y = MAX_Y;
      state.player.vy = 0;
      state.player.hold = false;
    }

    if (state.player.y <= 0) {
      state.player.y = 0;
      state.player.onGround = true;
      state.player.vy = 0;
    }
  }

  state.score += CONFIG.SCORE_PER_SEC * dt;
  updateScoreUI();

  state.spawnTimer += dt * 1000;
  if (state.spawnTimer >= state.nextSpawnDelay) {
    spawnMonster();
    scheduleNextSpawn();
  }

  checkCollisions();
  renderPlayer();

  state.rafId = requestAnimationFrame(gameLoop);
}

function checkCollisions() {
  const { collisionInset } = getDifficultyParams(state.elapsedS);
  const mikeRect = $mike.getBoundingClientRect();

  getMonsters().forEach(mon => {
    const r = mon.getBoundingClientRect();
    if (isHit(mikeRect, r, collisionInset)) gameOver();
  });
}

function spawnMonster() {
  if (state.phase !== STATE.RUNNING) return;

  const el = document.createElement("div");
  el.className = "monster";

  const pick = MONSTERS[Math.floor(Math.random() * MONSTERS.length)];
  el.textContent = pick;

  el.style.bottom = monsterBaseOffset(pick) + "px";

  if (Math.random() < 0.25) el.classList.add("alt");

  const diff = getDifficultyParams(state.elapsedS);
  const dur = rand(diff.monsterAnim.min, diff.monsterAnim.max);
  el.style.animationDuration = `${dur.toFixed(2)}s`;

  el.addEventListener("animationend", () => el.remove());
  $game.appendChild(el);
}

function jump() {
  if (!state.player.onGround) return;

  state.player.onGround = false;
  state.player.jumping = true;
  state.player.vy = CONFIG.jumpForce;

  state.player.hold = true;
  state.player.holdTimer = CONFIG.jumpHoldTime;
}

$game.addEventListener("pointerdown", () => {
  if (state.phase !== STATE.RUNNING) startGame();
  else jump();
}, { passive: true });

document.addEventListener("keydown", e => {
  if (e.code === "Space") {
    e.preventDefault();
    if (state.phase !== STATE.RUNNING) startGame();
    else jump();
  }
});

$retry.addEventListener("click", () => {
  clearMonsters();
  state.phase = STATE.IDLE;
  startGame();
});

window.addEventListener("load", () => {
  $game.focus();
});
