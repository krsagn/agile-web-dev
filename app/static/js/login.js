document.addEventListener("DOMContentLoaded", () => {
  const toggleButton = document.querySelector("[data-password-toggle]");
  const passwordInput = document.querySelector("#password");
  const facts = [
    {
      category: "Streaks",
      title: "Daily Quiz resets the challenge, not your momentum.",
      text: "A new daily quiz gives players a clean shot each day while still rewarding consistency and repeat play.",
      highlight: "Keeping a streak turns short quiz sessions into a long-term learning habit.",
      metrics: [
        { value: "24 hrs", label: "New challenge" },
        { value: "1 play", label: "Easy to start" },
        { value: "1 streak", label: "Worth keeping" }
      ]
    },
    {
      category: "Learning",
      title: "Daily Quiz makes revision feel more like a game round.",
      text: "Small, repeatable quiz sessions reduce the friction of studying and make it easier to come back tomorrow.",
      highlight: "Frequent retrieval practice can help facts stick better than rereading alone.",
      metrics: [
        { value: "5 min", label: "Quick challenge" },
        { value: "10 Qs", label: "Fast rounds" },
        { value: "Daily", label: "Built for habit" }
      ]
    },
    {
      category: "Competition",
      title: "A daily leaderboard gives every player a fresh chance to win.",
      text: "Because the quiz changes each day, new players can jump in without feeling permanently behind older accounts.",
      highlight: "Short competitive loops help keep the app welcoming for both casual and returning players.",
      metrics: [
        { value: "1 board", label: "Fresh ranking" },
        { value: "New day", label: "New chance" },
        { value: "All skill", label: "Fairer feel" }
      ]
    },
    {
      category: "Retention",
      title: "Daily Quiz works best when the reward loop is simple.",
      text: "A clear prompt, a quick play session, and a visible reward are often enough to bring learners back regularly.",
      highlight: "The most effective daily quiz flows are easy to begin and satisfying to finish.",
      metrics: [
        { value: "1 tap", label: "Start quickly" },
        { value: "Clear XP", label: "Visible reward" },
        { value: "Repeat", label: "Return tomorrow" }
      ]
    }
  ];
  const selectedFact = facts[Math.floor(Math.random() * facts.length)];
  const factCategory = document.querySelector("#factCategory");
  const factTitle = document.querySelector("#factTitle");
  const factText = document.querySelector("#factText");
  const factHighlight = document.querySelector("#factHighlight");
  const factMetricOneValue = document.querySelector("#factMetricOneValue");
  const factMetricOneLabel = document.querySelector("#factMetricOneLabel");
  const factMetricTwoValue = document.querySelector("#factMetricTwoValue");
  const factMetricTwoLabel = document.querySelector("#factMetricTwoLabel");
  const factMetricThreeValue = document.querySelector("#factMetricThreeValue");
  const factMetricThreeLabel = document.querySelector("#factMetricThreeLabel");

  if (
    selectedFact &&
    factCategory &&
    factTitle &&
    factText &&
    factHighlight &&
    factMetricOneValue &&
    factMetricOneLabel &&
    factMetricTwoValue &&
    factMetricTwoLabel &&
    factMetricThreeValue &&
    factMetricThreeLabel
  ) {
    factCategory.textContent = selectedFact.category;
    factTitle.textContent = selectedFact.title;
    factText.textContent = selectedFact.text;
    factHighlight.textContent = selectedFact.highlight;
    factMetricOneValue.textContent = selectedFact.metrics[0].value;
    factMetricOneLabel.textContent = selectedFact.metrics[0].label;
    factMetricTwoValue.textContent = selectedFact.metrics[1].value;
    factMetricTwoLabel.textContent = selectedFact.metrics[1].label;
    factMetricThreeValue.textContent = selectedFact.metrics[2].value;
    factMetricThreeLabel.textContent = selectedFact.metrics[2].label;
  }

  if (!toggleButton || !passwordInput) {
    return;
  }

  toggleButton.addEventListener("click", () => {
    const isPassword = passwordInput.getAttribute("type") === "password";
    const icon = toggleButton.querySelector("i");

    passwordInput.setAttribute("type", isPassword ? "text" : "password");
    toggleButton.setAttribute(
      "aria-label",
      isPassword ? "Hide password" : "Show password"
    );

    if (icon) {
      icon.className = isPassword ? "bi bi-eye-slash" : "bi bi-eye";
    }
  });
});
