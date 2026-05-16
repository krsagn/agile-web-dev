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
  console.log("register.js loaded, password validation v5");

  const toggleButtons = document.querySelectorAll("[data-password-toggle]");
  const popupLinks = document.querySelectorAll("[data-popup-link]");
  const registerForm = document.querySelector("#registerForm");

  const firstNameInput = document.querySelector("#firstName");
  const lastNameInput = document.querySelector("#lastName");
  const emailInput = document.querySelector("#registerEmail");
  const usernameInput = document.querySelector("#registerUsername");
  const passwordInput = document.querySelector("#registerPassword");
  const confirmPasswordInput = document.querySelector("#confirmPassword");

  const firstNameStatusText = document.querySelector("#firstNameStatusText");
  const lastNameStatusText = document.querySelector("#lastNameStatusText");
  const emailStatusText = document.querySelector("#emailStatusText");
  const usernameStatusText = document.querySelector("#usernameStatusText");
  const passwordStrengthBar = document.querySelector("#passwordStrengthBar");
  const passwordStrengthText = document.querySelector("#passwordStrengthText");
  const passwordMatchText = document.querySelector("#passwordMatchText");
  const termsStatusText = document.querySelector("#termsStatusText");

  const termsCheckbox = document.querySelector("#termsAccepted");
  const termsReadStatus = document.querySelector("#termsReadStatus");
  const createAccountButton = document.querySelector("#createAccountButton");

  let firstNameValid = false;
  let lastNameValid = false;
  let emailValid = false;
  let usernameValid = false;
  let passwordStrengthValid = false;
  let passwordMatchValid = false;
  let hasReadTerms = false;
  let usernameTimer = null;

  const commonPasswords = [
    "password",
    "password1",
    "password123",
    "1234",
    "12345",
    "123456",
    "1234567",
    "12345678",
    "123456789",
    "111111",
    "000000",
    "qwerty",
    "qwerty123",
    "abc123",
    "admin",
    "admin123",
    "letmein",
    "welcome",
    "iloveyou",
    "monkey",
    "dragon",
    "quokka",
    "quokka123"
  ];

  const weakWords = [
    "password",
    "qwerty",
    "admin",
    "welcome",
    "letmein",
    "quokka"
  ];

  const setStatus = (element, message, type) => {
    if (!element) {
      return;
    }

    element.textContent = message;
    element.classList.remove(
      "text-success",
      "text-danger",
      "text-warning",
      "text-muted"
    );

    if (type === "success") {
      element.classList.add("text-success");
    } else if (type === "danger") {
      element.classList.add("text-danger");
    } else if (type === "warning") {
      element.classList.add("text-warning");
    } else {
      element.classList.add("text-muted");
    }
  };

  const updateSubmitState = () => {
    if (!createAccountButton || !termsCheckbox || !termsReadStatus) {
      return;
    }

    const termsAccepted = hasReadTerms && termsCheckbox.checked;

    const formValid =
      firstNameValid &&
      lastNameValid &&
      emailValid &&
      usernameValid &&
      passwordStrengthValid &&
      passwordMatchValid &&
      termsAccepted;

    createAccountButton.disabled = !formValid;
  };

  const hasRepeatedCharacters = (password) => {
    return /(.)\1{2,}/.test(password);
  };

  const hasOnlyNumbers = (password) => {
    return /^[0-9]+$/.test(password);
  };

  const hasSimpleSequence = (password) => {
    const lowerPassword = password.toLowerCase();

    const sequences = [
      "1234",
      "2345",
      "3456",
      "4567",
      "5678",
      "6789",
      "9876",
      "8765",
      "7654",
      "6543",
      "5432",
      "4321",
      "abcd",
      "bcde",
      "cdef",
      "defg",
      "qwer",
      "wert",
      "erty",
      "asdf",
      "sdfg",
      "dfgh",
      "zxcv",
      "xcvb"
    ];

    return sequences.some((sequence) => lowerPassword.includes(sequence));
  };

  const containsWeakWord = (password) => {
    const lowerPassword = password.toLowerCase();

    return weakWords.some((word) => lowerPassword.includes(word));
  };

  const containsUserInfo = (password) => {
    const lowerPassword = password.toLowerCase();

    const username = usernameInput
      ? usernameInput.value.trim().toLowerCase()
      : "";

    const email = emailInput
      ? emailInput.value.trim().toLowerCase()
      : "";

    const emailName = email.includes("@") ? email.split("@")[0] : "";

    const containsUsername =
      username.length >= 2 && lowerPassword.includes(username);

    const containsEmailName =
      emailName.length >= 2 && lowerPassword.includes(emailName);

    return containsUsername || containsEmailName;
  };

  const checkFirstName = () => {
    if (!firstNameInput) {
      firstNameValid = true;
      updateSubmitState();
      return;
    }

    const firstName = firstNameInput.value.trim();
    firstNameValid = firstName.length > 0;

    if (firstNameValid) {
      setStatus(firstNameStatusText, "First name looks good.", "success");
    } else {
      setStatus(firstNameStatusText, "First name is required.", "danger");
    }

    updateSubmitState();
  };

  const checkLastName = () => {
    if (!lastNameInput) {
      lastNameValid = true;
      updateSubmitState();
      return;
    }

    const lastName = lastNameInput.value.trim();
    lastNameValid = lastName.length > 0;

    if (lastNameValid) {
      setStatus(lastNameStatusText, "Last name looks good.", "success");
    } else {
      setStatus(lastNameStatusText, "Last name is required.", "danger");
    }

    updateSubmitState();
  };

  const checkEmail = () => {
    if (!emailInput) {
      emailValid = true;
      updateSubmitState();
      return;
    }

    const email = emailInput.value.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    emailValid = emailPattern.test(email);

    if (!email) {
      setStatus(emailStatusText, "Email is required.", "danger");
    } else if (!emailValid) {
      setStatus(emailStatusText, "Enter a valid email address.", "danger");
    } else {
      setStatus(emailStatusText, "Email looks good.", "success");
    }

    updateSubmitState();
  };

  const checkUsername = () => {
    if (!usernameInput) {
      usernameValid = true;
      updateSubmitState();
      return;
    }

    const username = usernameInput.value.trim();

    clearTimeout(usernameTimer);

    if (username.length < 2) {
      usernameValid = false;
      setStatus(usernameStatusText, "Type at least 2 characters.", "danger");
      updateSubmitState();
      return;
    }

    setStatus(usernameStatusText, "Checking username...", "muted");

    usernameTimer = setTimeout(async () => {
      try {
        const response = await fetch(
          `/api/check-username?u=${encodeURIComponent(username)}`
        );

        if (!response.ok) {
          usernameValid = true;
          setStatus(
            usernameStatusText,
            "Username length looks good. Server will verify when submitted.",
            "success"
          );
          updateSubmitState();
          return;
        }

        const data = await response.json();
        usernameValid = Boolean(data.available);

        if (usernameValid) {
          setStatus(usernameStatusText, "Username is available.", "success");
        } else {
          setStatus(usernameStatusText, "Username is already taken.", "danger");
        }
      } catch (error) {
        usernameValid = true;
        setStatus(
          usernameStatusText,
          "Username length looks good. Server will verify when submitted.",
          "success"
        );
      }

      updateSubmitState();
    }, 250);
  };

  const checkPasswordStrength = () => {
    if (!passwordInput) {
      passwordStrengthValid = false;
      updateSubmitState();
      return;
    }

    if (!passwordStrengthBar || !passwordStrengthText) {
      console.error("Missing password strength feedback elements in register.html");
      passwordStrengthValid = false;
      updateSubmitState();
      return;
    }

    const password = passwordInput.value;
    const lowerPassword = password.toLowerCase();

    let score = 0;
    const issues = [];

    if (password.length >= 12) {
      score += 2;
    } else if (password.length >= 8) {
      score += 1;
    } else {
      issues.push("use at least 8 characters");
    }

    if (/[A-Z]/.test(password)) {
      score += 1;
    } else {
      issues.push("add an uppercase letter");
    }

    if (/[a-z]/.test(password)) {
      score += 1;
    } else {
      issues.push("add a lowercase letter");
    }

    if (/[0-9]/.test(password)) {
      score += 1;
    } else {
      issues.push("add a number");
    }

    if (/[^A-Za-z0-9]/.test(password)) {
      score += 1;
    } else {
      issues.push("add a symbol");
    }

    const isCommonPassword = commonPasswords.includes(lowerPassword);
    const usesWeakWord = containsWeakWord(password);
    const usesRepeatedCharacters = hasRepeatedCharacters(password);
    const usesSimpleSequence = hasSimpleSequence(password);
    const usesOnlyNumbers = hasOnlyNumbers(password);
    const usesUserInfo = containsUserInfo(password);

    if (isCommonPassword) {
      issues.push("avoid common passwords");
    }

    if (usesWeakWord) {
      issues.push("avoid obvious words");
    }

    if (usesRepeatedCharacters) {
      issues.push("avoid repeated characters");
    }

    if (usesSimpleSequence) {
      issues.push("avoid simple sequences");
    }

    if (usesOnlyNumbers) {
      issues.push("do not use only numbers");
    }

    if (usesUserInfo) {
      issues.push("do not include your username or email");
    }

    const hasCriticalWeakness =
      isCommonPassword ||
      usesWeakWord ||
      usesRepeatedCharacters ||
      usesSimpleSequence ||
      usesOnlyNumbers ||
      usesUserInfo;

    passwordStrengthBar.classList.remove(
      "bg-danger",
      "bg-warning",
      "bg-success"
    );

    if (!password) {
      passwordStrengthValid = false;
      passwordStrengthBar.style.width = "0%";
      setStatus(
        passwordStrengthText,
        "Enter a password to check strength.",
        "muted"
      );
    } else if (score < 4 || hasCriticalWeakness) {
      passwordStrengthValid = false;
      passwordStrengthBar.style.width = "33%";
      passwordStrengthBar.classList.add("bg-danger");

      const uniqueIssues = [...new Set(issues)];
      const issueText = uniqueIssues.slice(0, 3).join(", ");

      setStatus(
        passwordStrengthText,
        `Password is too easy. Please ${issueText}.`,
        "danger"
      );
    } else if (score < 6) {
      passwordStrengthValid = true;
      passwordStrengthBar.style.width = "66%";
      passwordStrengthBar.classList.add("bg-warning");
      setStatus(
        passwordStrengthText,
        "Medium password. Stronger is recommended.",
        "warning"
      );
    } else {
      passwordStrengthValid = true;
      passwordStrengthBar.style.width = "100%";
      passwordStrengthBar.classList.add("bg-success");
      setStatus(passwordStrengthText, "Strong password.", "success");
    }

    checkPasswordMatch();
    updateSubmitState();
  };

  const checkPasswordMatch = () => {
    if (!passwordInput || !confirmPasswordInput || !passwordMatchText) {
      passwordMatchValid = false;
      updateSubmitState();
      return;
    }

    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    if (!confirmPassword) {
      passwordMatchValid = false;
      setStatus(passwordMatchText, "Confirm your password.", "muted");
    } else if (password === confirmPassword) {
      passwordMatchValid = true;
      setStatus(passwordMatchText, "Passwords match.", "success");
    } else {
      passwordMatchValid = false;
      setStatus(passwordMatchText, "Passwords do not match.", "danger");
    }

    updateSubmitState();
  };

  const syncTermsState = (readTerms) => {
    if (!termsCheckbox || !termsReadStatus) {
      return;
    }

    hasReadTerms = readTerms;
    termsCheckbox.disabled = !hasReadTerms;
    termsReadStatus.value = hasReadTerms ? "yes" : "no";

    if (hasReadTerms) {
      termsCheckbox.checked = true;
      setStatus(termsStatusText, "Terms accepted.", "success");
    } else {
      termsCheckbox.checked = false;
      setStatus(
        termsStatusText,
        "Read and accept the terms to create your account.",
        "muted"
      );
    }

    updateSubmitState();
  };

  toggleButtons.forEach((button) => {
    const targetId = button.getAttribute("data-password-toggle");
    const passwordInputTarget = targetId
      ? document.getElementById(targetId)
      : null;

    if (!passwordInputTarget) {
      return;
    }

    button.addEventListener("click", () => {
      const isPassword = passwordInputTarget.getAttribute("type") === "password";
      const icon = button.querySelector("i");

      passwordInputTarget.setAttribute("type", isPassword ? "text" : "password");
      button.setAttribute(
        "aria-label",
        isPassword ? "Hide password" : "Show password"
      );

      if (icon) {
        icon.className = isPassword ? "bi bi-eye-slash" : "bi bi-eye";
      }
    });
  });

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

  if (firstNameInput) {
    firstNameInput.addEventListener("input", checkFirstName);
  }

  if (lastNameInput) {
    lastNameInput.addEventListener("input", checkLastName);
  }

  if (emailInput) {
    emailInput.addEventListener("input", () => {
      checkEmail();
      checkPasswordStrength();
    });
  }

  if (usernameInput) {
    usernameInput.addEventListener("input", () => {
      checkUsername();
      checkPasswordStrength();
    });
  }

  if (passwordInput) {
    passwordInput.addEventListener("input", checkPasswordStrength);
  }

  if (confirmPasswordInput) {
    confirmPasswordInput.addEventListener("input", checkPasswordMatch);
  }

  if (termsCheckbox) {
    termsCheckbox.addEventListener("change", updateSubmitState);
  }

  if (registerForm) {
    registerForm.addEventListener("submit", (event) => {
      checkFirstName();
      checkLastName();
      checkEmail();
      checkUsername();
      checkPasswordStrength();
      checkPasswordMatch();
      updateSubmitState();

      if (createAccountButton && createAccountButton.disabled) {
        event.preventDefault();
      }
    });
  }

  syncTermsState(false);
  checkFirstName();
  checkLastName();
  checkEmail();
  checkUsername();
  checkPasswordStrength();
  checkPasswordMatch();
});