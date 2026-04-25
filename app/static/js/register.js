document.addEventListener("DOMContentLoaded", () => {
  const toggleButtons = document.querySelectorAll("[data-password-toggle]");

  toggleButtons.forEach((button) => {
    const targetId = button.getAttribute("data-password-toggle");
    const passwordInput = targetId
      ? document.getElementById(targetId)
      : null;

    if (!passwordInput) {
      return;
    }

    button.addEventListener("click", () => {
      const isPassword = passwordInput.getAttribute("type") === "password";
      const icon = button.querySelector("i");

      passwordInput.setAttribute("type", isPassword ? "text" : "password");
      button.setAttribute(
        "aria-label",
        isPassword ? "Hide password" : "Show password"
      );

      if (icon) {
        icon.className = isPassword ? "bi bi-eye-slash" : "bi bi-eye";
      }
    });
  });
});
