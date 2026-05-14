document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("user-search-input")
  const resultsContainer = document.getElementById("user-search-results")
  const messageContainer = document.getElementById("user-search-message")

  let searchTimeout = null

  function showMessage(message, type = "warning") {
    messageContainer.innerHTML = `
      <div class="alert alert-${type} text-center" role="alert">
        ${message}
      </div>
    `
  }

  function clearMessage() {
    messageContainer.innerHTML = ""
  }

  function clearResults() {
    resultsContainer.innerHTML = ""
  }

  function renderUsers(users) {
    clearResults()

    if (users.length === 0) {
      showMessage("No users found.", "warning")
      return
    }

    clearMessage()

    users.forEach(function (user) {
      const userCard = document.createElement("a")

      userCard.href = user.profile_url
      userCard.className = "user-result-card"

      userCard.innerHTML = `
        <div class="user-result-left">
          <div class="user-avatar">
            ${user.username.charAt(0).toUpperCase()}
          </div>

          <div>
            <div class="user-name">
              ${user.full_name}
              ${user.is_current_user ? "<span class='badge bg-primary ms-2'>You</span>" : ""}
            </div>

            <p class="user-username">
              @${user.username}
            </p>
          </div>
        </div>

        <div class="user-meta">
          <div>Level ${user.level}</div>
          <div>${user.title}</div>
          <div>${user.xp} XP</div>
        </div>
      `

      resultsContainer.appendChild(userCard)
    })
  }

  async function searchUsers(query) {
    if (query.length < 2) {
      clearResults()
      clearMessage()
      return
    }

    try {
      const response = await fetch(
        `/api/users/search?q=${encodeURIComponent(query)}`
      )

      const data = await response.json()

      if (!response.ok || !data.success) {
        showMessage("Unable to search users.", "danger")
        return
      }

      renderUsers(data.users)

    } catch (error) {
      console.error("Error searching users:", error)
      showMessage("Error searching users. Please try again.", "danger")
    }
  }

  searchInput.addEventListener("input", function () {
    const query = searchInput.value.trim()

    clearTimeout(searchTimeout)

    searchTimeout = setTimeout(function () {
      searchUsers(query)
    }, 300)
  })
})