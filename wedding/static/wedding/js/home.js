(function () {
  const data = window.HOME_DATA || {};
  const weddingDate = new Date(data.weddingDate).getTime();

  const elDays = document.getElementById("days");
  const elHours = document.getElementById("hours");
  const elMinutes = document.getElementById("minutes");
  const elSeconds = document.getElementById("seconds");

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function tick() {
    const now = Date.now();
    let distance = weddingDate - now;

    if (distance < 0) distance = 0;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    if (elDays) elDays.textContent = days;
    if (elHours) elHours.textContent = pad2(hours);
    if (elMinutes) elMinutes.textContent = pad2(minutes);
    if (elSeconds) elSeconds.textContent = pad2(seconds);
  }

  tick();
  setInterval(tick, 1000);
})();