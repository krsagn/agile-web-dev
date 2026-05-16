import threading
import unittest
from datetime import datetime, timezone

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy.pool import StaticPool
from werkzeug.security import generate_password_hash
from werkzeug.serving import make_server

from app import create_app
from app.config import TestingConfig
from app.models import db, RegisteredUser, QuizResult, UserAchievement


class SeleniumTestingConfig(TestingConfig):
    """
    Extends TestingConfig with StaticPool so that all SQLAlchemy connections
    (main thread and server thread) reuse the same in-memory SQLite connection.
    Without this, each thread gets its own empty database.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }


HOST = "localhost"
PORT = 5001
BASE_URL = f"http://{HOST}:{PORT}"

_TEST_USER = {
    "first_name": "Test",
    "last_name": "User",
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
}

_OTHER_USER = {
    "first_name": "Other",
    "last_name": "Person",
    "username": "otheruser",
    "email": "other@example.com",
    "password": "otherpass123",
}


class SeleniumTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(SeleniumTestingConfig)
        cls.app_ctx = cls.app.app_context()
        cls.app_ctx.push()
        db.create_all()

        # Populate quiz questions once for the whole suite
        with cls.app.app_context():
            from app.db import add_sample_quizzes
            add_sample_quizzes()

        # Start Flask in a background thread so Selenium has a real server to hit
        cls.server = make_server(HOST, PORT, cls.app)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        db.session.remove()
        db.drop_all()
        cls.app_ctx.pop()

    def _make_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # A roomy viewport keeps form submit buttons above the fold on tall pages
        options.add_argument("--window-size=1400,2000")
        return webdriver.Chrome(options=options)

    def setUp(self):
        """Clean DB state and start a fresh Chrome driver before every test.

        We create the driver last. If the DB setup blows up, unittest won't
        run tearDown, so an early-launched Chrome would just sit there
        orphaned. Doing the DB work first means a setup failure costs nothing.
        """
        UserAchievement.query.delete()
        QuizResult.query.delete()
        RegisteredUser.query.delete()
        db.session.commit()

        user = RegisteredUser(
            first_name=_TEST_USER["first_name"],
            last_name=_TEST_USER["last_name"],
            username=_TEST_USER["username"],
            email=_TEST_USER["email"],
            password_hash=generate_password_hash(_TEST_USER["password"]),
            terms_read=True,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(user)
        db.session.commit()
        self._user_id = user.id

        self.driver = self._make_driver()

    def tearDown(self):
        self.driver.quit()

    def _login(self):
        """Log in as the test user and wait until the profile page loads."""
        self.driver.get(f"{BASE_URL}/login")
        self.driver.find_element(By.ID, "identifier").send_keys(_TEST_USER["username"])
        self.driver.find_element(By.ID, "password").send_keys(_TEST_USER["password"])
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/profile"))

    # ------------------------------------------------------------------
    # Test 1: Registration
    # Covers user data persisted between sessions, HTML form handling,
    # and CSRF tokens flowing through the registration template.
    # ------------------------------------------------------------------

    def test_01_register_redirects_to_login_with_success_message(self):
        self.driver.get(f"{BASE_URL}/register")

        self.driver.find_element(By.ID, "firstName").send_keys("New")
        self.driver.find_element(By.ID, "lastName").send_keys("User")
        self.driver.find_element(By.ID, "registerEmail").send_keys("new@example.com")
        self.driver.find_element(By.ID, "registerUsername").send_keys("newuser")
        self.driver.find_element(By.ID, "registerPassword").send_keys("password123")
        self.driver.find_element(By.ID, "confirmPassword").send_keys("password123")

        # The terms checkbox and submit button stay disabled until the user
        # reads the Terms popup in a separate browser window. We skip that UI
        # flow with JavaScript, setting the hidden field the server checks
        # and enabling the submit button. That's exactly what the popup's
        # postMessage callback would do.
        self.driver.execute_script("""
            document.getElementById('termsReadStatus').value = 'yes';
            document.getElementById('termsAccepted').disabled = false;
            document.getElementById('termsAccepted').checked = true;
            document.getElementById('createAccountButton').disabled = false;
        """)

        self.driver.find_element(By.ID, "createAccountButton").click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("/login"))

        alert = self.driver.find_element(By.CSS_SELECTOR, ".alert.alert-success")
        self.assertIn("Account created successfully", alert.text)

        # Verify the rubric line directly. The new user should actually be
        # in the DB, not just confirmed by a flash message on the page.
        persisted = RegisteredUser.query.filter_by(username="newuser").first()
        self.assertIsNotNone(persisted)
        self.assertEqual(persisted.email, "new@example.com")

    # ------------------------------------------------------------------
    # Test 2: Login then logout
    # Covers the "Login and logout" key requirement. Also checks the
    # session is cleared, so a protected page bounces back to /login
    # afterwards.
    # ------------------------------------------------------------------

    def test_02_login_and_logout(self):
        self._login()
        self.assertIn("/profile", self.driver.current_url)

        # Wait for the profile page to fully render before clicking logout.
        # This gives the page a chance to consume the login-success flash,
        # so it doesn't survive in the session cookie and bleed through to
        # the post-logout /login page.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-title"))
        )

        # Click the logout link in the authenticated sidebar
        self.driver.find_element(By.CSS_SELECTOR, "a[href$='/logout']").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login"))

        # The profile page doesn't consume flashed messages, so both the
        # login-success and logout-success flashes can appear here together.
        # Use XPath to grab the alert that actually mentions logout.
        logout_alert = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[contains(@class,'alert-success') and contains(.,'Logged out successfully')]"
            ))
        )
        self.assertIn("Logged out successfully", logout_alert.text)

        # A login-required page should now redirect back to /login
        self.driver.get(f"{BASE_URL}/profile")
        WebDriverWait(self.driver, 10).until(EC.url_contains("/login"))

    # ------------------------------------------------------------------
    # Test 3: Complete quiz end-to-end
    # Covers AJAX/JS, non-trivial Flask data manipulation, and DB write
    # persistence by checking the quiz result actually saves.
    # ------------------------------------------------------------------

    def test_03_complete_quiz_shows_results_page(self):
        self._login()
        self.driver.get(f"{BASE_URL}/quiz")

        # Pick a category and confirm it
        self.driver.find_element(
            By.CSS_SELECTOR, ".category-btn[data-category='Science']"
        ).click()
        self.driver.find_element(By.ID, "confirm-category-btn").click()

        # The quiz content div is hidden with d-none until the JS fetch
        # returns.
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "quiz-content"))
        )

        # Record an answer on question 1 so the submission has real content,
        # then drive the quiz to completion by calling the Next button's click
        # handler ten times in a row from inside the page. The first nine
        # clicks just advance currentQuestion via loadQuestion, the tenth lands
        # on the last question and triggers finishQuiz, which POSTs to
        # /api/submit-quiz and redirects to /results. Driving it from JS avoids
        # the flakiness of issuing ten Selenium clicks back-to-back, where
        # Chrome occasionally drops one under load.
        self.driver.find_element(
            By.CSS_SELECTOR, ".option-card[data-option='A']"
        ).click()

        self.driver.execute_script("""
            const nextBtn = document.getElementById('next-btn');
            for (let i = 0; i < 10; i++) {
                nextBtn.click();
            }
        """)

        # The final next-btn click invokes finishQuiz, which POSTs to
        # /api/submit-quiz and then redirects to /results.
        WebDriverWait(self.driver, 10).until(EC.url_contains("/results"))

        # Verify the rubric line directly. A QuizResult row should actually
        # be in the DB. The score-display element is in the template's
        # static HTML with an initial text of "0", so its mere presence
        # wouldn't prove the data path. Checking the DB row does.
        db.session.expire_all()
        result = QuizResult.query.filter_by(user_id=self._user_id).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.total, 10)
        self.assertEqual(result.category, "Science")

    # ------------------------------------------------------------------
    # Test 4: View another user's public profile
    # Covers the "Users can view other users' data" key requirement.
    # Also exercises the public profile page, login-required guard, and
    # a DB read across users.
    # ------------------------------------------------------------------

    def test_04_view_other_user_profile(self):
        # Seed a second user whose profile the test user will visit
        other = RegisteredUser(
            first_name=_OTHER_USER["first_name"],
            last_name=_OTHER_USER["last_name"],
            username=_OTHER_USER["username"],
            email=_OTHER_USER["email"],
            password_hash=generate_password_hash(_OTHER_USER["password"]),
            terms_read=True,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(other)
        db.session.commit()

        self._login()
        self.driver.get(f"{BASE_URL}/users/{_OTHER_USER['username']}")

        # Profile name heading should show the other user's full name
        name_el = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-name"))
        )
        self.assertIn(_OTHER_USER["first_name"], name_el.text)
        self.assertIn(_OTHER_USER["last_name"], name_el.text)

        # Username handle should also appear
        username_el = self.driver.find_element(By.CSS_SELECTOR, ".profile-username")
        self.assertIn(_OTHER_USER["username"], username_el.text)

    # ------------------------------------------------------------------
    # Test 5: CSRF protection rejects requests without a valid token
    # Covers the "CSRF tokens on ALL forms" security rubric line.
    # We turn CSRF on just for this test. The rest of the suite inherits
    # WTF_CSRF_ENABLED=False from TestingConfig for speed.
    # ------------------------------------------------------------------

    def test_05_login_without_csrf_token_is_rejected(self):
        self.app.config["WTF_CSRF_ENABLED"] = True
        try:
            self.driver.get(f"{BASE_URL}/login")

            # Remove the hidden csrf_token input before submitting, so the
            # server receives a POST with no token at all.
            self.driver.execute_script(
                "document.querySelector(\"input[name='csrf_token']\").remove();"
            )

            self.driver.find_element(By.ID, "identifier").send_keys(_TEST_USER["username"])
            self.driver.find_element(By.ID, "password").send_keys(_TEST_USER["password"])
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

            # Flask-WTF returns a 400 page that mentions the CSRF token.
            WebDriverWait(self.driver, 10).until(
                lambda d: "CSRF" in d.page_source or "Bad Request" in d.page_source
            )
            self.assertNotIn("/profile", self.driver.current_url)
        finally:
            self.app.config["WTF_CSRF_ENABLED"] = False


if __name__ == "__main__":
    unittest.main()
