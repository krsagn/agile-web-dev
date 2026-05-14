window.handleGoogleCredential = (response) => {
  if (!response || !response.credential) {
    return;
  }

  const form = document.createElement("form");
  const credentialInput = document.createElement("input");

  form.method = "post";
  form.action = "/auth/google";
  form.style.display = "none";

  credentialInput.type = "hidden";
  credentialInput.name = "credential";
  credentialInput.value = response.credential;

  form.appendChild(credentialInput);
  document.body.appendChild(form);
  form.submit();
};

document.addEventListener("DOMContentLoaded", () => {
  const toggleButtons = document.querySelectorAll("[data-password-toggle]");
  const popupLinks = document.querySelectorAll("[data-popup-link]");
  const registerForm = document.querySelector("#registerForm");
  const termsCheckbox = document.querySelector("#termsAccepted");
  const termsReadStatus = document.querySelector("#termsReadStatus");
  const createAccountButton = document.querySelector("#createAccountButton");

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

  const syncTermsState = (hasReadTerms) => {
    if (!termsCheckbox || !termsReadStatus || !createAccountButton) {
      return;
    }

    termsCheckbox.disabled = !hasReadTerms;
    termsReadStatus.value = hasReadTerms ? "yes" : "no";

    if (hasReadTerms) {
      termsCheckbox.checked = true;
      createAccountButton.disabled = false;
    } else {
      termsCheckbox.checked = false;
      createAccountButton.disabled = true;
    }
  };

  syncTermsState(false);

  popupLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();

      const width = 760;
      const height = 820;
      const left = window.screenX + (window.outerWidth - width) / 2;
      const top = window.screenY + (window.outerHeight - height) / 2;
      const features = [
        `width=${width}`,
        `height=${height}`,
        `left=${Math.max(0, left)}`,
        `top=${Math.max(0, top)}`,
        "resizable=yes",
        "scrollbars=yes"
      ].join(",");
      const popup = window.open(link.href, "quokka-terms", features);

      if (!popup) {
        window.location.href = link.href;
      }
    });
  });

  window.addEventListener("message", (event) => {
    if (event.origin !== window.location.origin) {
      return;
    }

    if (event.data && event.data.type === "quokka-terms-read") {
      syncTermsState(true);
    }
  });

  if (registerForm) {
    registerForm.addEventListener("submit", (event) => {
      const hasReadTerms = termsReadStatus && termsReadStatus.value === "yes";
      const hasAcceptedTerms = termsCheckbox && termsCheckbox.checked;

      if (!hasReadTerms || !hasAcceptedTerms) {
        event.preventDefault();
        syncTermsState(hasReadTerms);
      }
    });
  }
});
