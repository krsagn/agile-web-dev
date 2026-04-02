function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // For TESTING PURPOSES ONLY
    if (username === "admin" && password === "1234") {
        alert("Login successful!");
        // Redirect to dashboard or home page
        window.location.href = "pages/dashboard.html";
    } else {
        alert("Invalid username or password. Please try again.");
    }
}