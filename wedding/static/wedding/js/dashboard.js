(function () {
  const data = window.DASHBOARD_DATA || {};

  const timerEl = document.getElementById("timer");
  const weddingDate = new Date(data.weddingDate).getTime();

  function tick() {
    const now = new Date().getTime();
    let distance = weddingDate - now;

    if (distance < 0) distance = 0;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    if (timerEl) {
      timerEl.textContent =
        `${days}d ${String(hours).padStart(2, "0")}h ${String(minutes).padStart(2, "0")}m ${String(seconds).padStart(2, "0")}s`;
    }
  }

  tick();
  setInterval(tick, 1000);

  const totalPaid = Number(data.totalPaid || 0);
  const totalPending = Number(data.totalPending || 0);
  const confirmedGuests = Number(data.confirmedGuests || 0);
  const notConfirmed = Number(data.notConfirmed || 0);

  const categoryLabelsEl = document.getElementById("category-labels");
  const categoryValuesEl = document.getElementById("category-values");

  const categoryLabels = categoryLabelsEl
    ? JSON.parse(categoryLabelsEl.textContent)
    : [];

  const categoryValues = categoryValuesEl
    ? JSON.parse(categoryValuesEl.textContent)
    : [];

  const financeCanvas = document.getElementById("financeChart");
  if (financeCanvas) {
    new Chart(financeCanvas, {
      type: "doughnut",
      data: {
        labels: ["Pago", "Pendente"],
        datasets: [
          {
            data: [totalPaid, totalPending],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  const guestCanvas = document.getElementById("guestChart");
  if (guestCanvas) {
    new Chart(guestCanvas, {
      type: "doughnut",
      data: {
        labels: ["Confirmados", "Não confirmados"],
        datasets: [
          {
            data: [confirmedGuests, notConfirmed],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    });
  }

  const categoryCanvas = document.getElementById("categoryChart");
  if (categoryCanvas && categoryLabels.length > 0 && categoryValues.length > 0) {
    new Chart(categoryCanvas, {
      type: "bar",
      data: {
        labels: categoryLabels,
        datasets: [
          {
            label: "Gastos por categoria",
            data: categoryValues,
            borderRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  const openGuestFormBtn = document.getElementById("openGuestFormBtn");
  const guestFormWrapper = document.getElementById("guestFormWrapper");

  if (openGuestFormBtn && guestFormWrapper) {
    openGuestFormBtn.addEventListener("click", function () {
      guestFormWrapper.classList.toggle("hidden");
    });
  }

  const companionButtons = document.querySelectorAll(".companions-toggle");
  companionButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const targetId = button.getAttribute("data-target");
      const targetRow = document.getElementById(targetId);

      if (targetRow) {
        targetRow.classList.toggle("show");
      }
    });
  });

  const editButtons = document.querySelectorAll(".edit-btn");
  editButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const targetId = button.getAttribute("data-target");
      const targetRow = document.getElementById(targetId);

      if (targetRow) {
        targetRow.classList.toggle("show");
      }
    });
  });
})();