import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# --- CONFIGURATION ---
URL = "http://localhost:8000/login/index.php"
USERNAME = "admin"  # Or 'moodle' depending on your setup
PASSWORD = "SecretPass123!"   # Change this to your actual password (e.g., 'moodle', 'Admin123!')

# --- SETUP DRIVER ---
print("1. Launching Chrome Browser...")
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # --- STEP 1: OPEN LOGIN PAGE ---
    print("2. Navigating to Moodle Login Page...")
    driver.get(URL)
    time.sleep(2) # Wait for page to load

    # --- STEP 2: ENTER CREDENTIALS ---
    print(f"3. Entering Username: {USERNAME}")
    user_field = driver.find_element(By.ID, "username")
    user_field.clear()
    user_field.send_keys(USERNAME)

    print("4. Entering Password...")
    pass_field = driver.find_element(By.ID, "password")
    pass_field.clear()
    pass_field.send_keys(PASSWORD)

    # --- STEP 3: CLICK LOGIN ---
    print("5. Clicking Login Button...")
    login_btn = driver.find_element(By.ID, "loginbtn")
    login_btn.click()
    
    # Wait for Dashboard to load
    time.sleep(3)

    # --- STEP 4: VERIFY LOGIN (ASSERTION) ---
    print("6. Verifying Login Success...")
    page_title = driver.title
    print(f"   Current Page Title: {page_title}")

    # Check if 'Dashboard' or 'My courses' is in the title
    if "Dashboard" in page_title or "My courses" in page_title or "Home" in page_title:
        print("   ✅ TEST PASS: Login Successful!")
    else:
        print("   ❌ TEST FAIL: Login Failed or Title Mismatch.")

    # --- STEP 5: LOGOUT (OPTIONAL) ---
    # Note: Logout menus in Moodle vary by theme. 
    # Usually, you click the user menu (top right) then logout.
    # We will just verify the login for this script to keep it simple.

except Exception as e:
    print(f"   ❌ An error occurred: {e}")

finally:
    # --- CLEANUP ---
    print("7. Closing Browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
    print("   Test Completed.")