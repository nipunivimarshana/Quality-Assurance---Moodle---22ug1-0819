import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class MoodleTests(unittest.TestCase):

    # --- SETUP: Runs before EACH test ---
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10) # Intelligent wait
        self.base_url = "http://localhost:8000"
        self.username = "admin"
        self.password = "SecretPass123!" 

    # --- HELPER FUNCTION: To avoid repeating login code ---
    def login(self):
        driver = self.driver
        driver.get(f"{self.base_url}/login/index.php")
        driver.find_element(By.ID, "username").send_keys(self.username)
        driver.find_element(By.ID, "password").send_keys(self.password)
        driver.find_element(By.ID, "loginbtn").click()

    # --- TEST 1: Verify Login ---
# --- TEST 1: Verify Login ---
    def test_01_login_success(self):
        print("\n--- Running Test 1: Login Success ---")
        self.login()
        
        # Allow a moment for the Dashboard to load
        time.sleep(3)
        
        # Debugging: Print the title so we see what the browser sees
        print(f"   Current Page Title: {self.driver.title}")

        # Assertion: Check if "Dashboard" or the Site Name is in the title
        # This is more reliable than looking for a specific icon class
        is_logged_in = "Dashboard" in self.driver.title or "My courses" in self.driver.title or "Moodle" in self.driver.title
        
        self.assertTrue(is_logged_in, f"Login Verification Failed. Actual Title: {self.driver.title}")
        print("✅ Login Verified.")

    # --- TEST 2: Create a New Course (End-to-End) ---
    def test_02_create_course(self):
        print("\n--- Running Test 2: Create Course ---")
        self.login()

        # 1. Navigate directly to 'Add Course' page (Shortcut for stability)
        # Note: category=1 is the default 'Miscellaneous' category
        self.driver.get(f"{self.base_url}/course/edit.php?category=1")

        # 2. Generate unique course name so test can run multiple times
        unique_id = int(time.time())
        course_fullname = f"Selenium Auto Course {unique_id}"
        course_shortname = f"AUTO_{unique_id}"

        print(f"Creating Course: {course_fullname}")

        # 3. Fill Form
        self.driver.find_element(By.ID, "id_fullname").send_keys(course_fullname)
        self.driver.find_element(By.ID, "id_shortname").send_keys(course_shortname)

        # 4. Scroll down and Click 'Save and display'
        # Moodle buttons can be tricky, sometimes we need to scroll
        save_button = self.driver.find_element(By.ID, "id_saveanddisplay")
        self.driver.execute_script("arguments[0].scrollIntoView();", save_button)
        time.sleep(1) 
        save_button.click()

        # 5. Validation (Assertion)
        # Check if the page title contains the course name
        time.sleep(2)
        print(f"Page Title after save: {self.driver.title}")
        self.assertIn(course_fullname, self.driver.title, "Course creation failed!")
        print("✅ Course Created Successfully.")

    # --- TEARDOWN: Runs after EACH test ---
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()