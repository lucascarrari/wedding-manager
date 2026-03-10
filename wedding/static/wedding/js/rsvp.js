document.addEventListener("DOMContentLoaded", function () {
  const companionsCountInput = document.getElementById("id_companions_count");
  const companionFields = document.querySelectorAll(".companion-field");

  function updateCompanionFields() {
    const count = parseInt(companionsCountInput.value || 0, 10);

    companionFields.forEach((field) => {
      const index = parseInt(field.dataset.index, 10);
      const input = field.querySelector("input");

      if (index <= count) {
        field.classList.add("active");
      } else {
        field.classList.remove("active");
        if (input) {
          input.value = "";
        }
      }
    });
  }

  if (companionsCountInput) {
    companionsCountInput.addEventListener("input", updateCompanionFields);
    companionsCountInput.addEventListener("change", updateCompanionFields);
    updateCompanionFields();
  }
});