import os
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

try:
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

SKIP_SELENIUM = os.environ.get("SKIP_SELENIUM") == "1"


@unittest.skipIf(SKIP_SELENIUM, "SKIP_SELENIUM=1")
@unittest.skipUnless(SELENIUM_AVAILABLE, "selenium/webdriver-manager not installed")
class AdminSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            service = Service(ChromeDriverManager().install())
            cls.driver = Chrome(service=service, options=options)
        except Exception as exc:
            super().tearDownClass()
            raise unittest.SkipTest(f"Chrome недоступен: {exc}")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()
        super().tearDownClass()

    def test_admin_login_form(self):
        self.driver.get(self.live_server_url + "/admin/login/")
        username = self.driver.find_element(By.NAME, "username")
        username.send_keys("admin")
        self.assertEqual(username.get_attribute("value"), "admin")

        password = self.driver.find_element(By.NAME, "password")
        password.send_keys("wrong")

        submit = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit.click()

        self.assertIn("/admin/", self.driver.current_url)
