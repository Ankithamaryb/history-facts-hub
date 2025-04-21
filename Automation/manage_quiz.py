from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time

# Edge setup
options = Options()
options.add_argument('--start-maximized')
service = Service()
driver = webdriver.Edge(service=service, options=options)

try:
    print("📍 Opening admin login page...")
    driver.get("http://127.0.0.1:5000/login")
    print("📍 Logging in as admin...")
    driver.find_element(By.NAME, "username").send_keys("admin123")
    driver.find_element(By.NAME, "password").send_keys("adminpass")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()

    print("📍 Waiting for dashboard...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Manage Quiz"))
    )

    print("📍 Navigating to 'Manage Quiz'...")
    driver.find_element(By.LINK_TEXT, "Manage Quiz").click()

    print("📍 Waiting for table to load...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table')]"))
    )

    print("📍 Verifying that quiz questions are displayed...")
    table = driver.find_element(By.XPATH, "//table[contains(@class, 'table')]")
    rows = table.find_elements(By.XPATH, ".//tbody//tr")
    if rows:
        print(f"✅ Found {len(rows)} quiz questions.")
    else:
        print("❌ No quiz questions found.")

    print("📍 Clicking 'Add New Question' button...")
    add_question_btn = driver.find_element(By.LINK_TEXT, "Add New Question")
    add_question_btn.click()

    print("📍 Filling in 'Add Quiz' form...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Add Quiz')]"))
    )

    driver.find_element(By.NAME, "question").send_keys("In which year was COVID-19 declared a pandemic by the WHO?")
    driver.find_element(By.NAME, "option1").send_keys("2019")
    driver.find_element(By.NAME, "option2").send_keys("2020")
    driver.find_element(By.NAME, "option3").send_keys("2021")
    driver.find_element(By.NAME, "answer").send_keys("2020")

    print("📍 Submitting the form using the 'Add' button...")
    add_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Add')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
    time.sleep(1)
    add_btn.click()

    print("📍 Waiting for redirection and checking if the question is added...")
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/manage_quiz"))
    time.sleep(1)

    page_source = driver.page_source
    if "In which year was COVID-19 declared a pandemic by the WHO?" in page_source:
        print("✅ Quiz question added successfully by admin!")
    else:
        print("❌ Quiz question not found after submission.")

    print("📍 Editing the recently added quiz question...")
    edit_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Edit')]")
    edit_btn.click()

    print("📍 Waiting for the edit page...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "question"))
    )

    driver.find_element(By.NAME, "question").clear()
    driver.find_element(By.NAME, "question").send_keys("When did WHO declare COVID-19 a pandemic?")

    print("📍 Submitting the edited question...")
    update_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Update')]")
    update_btn.click()

    print("📍 Waiting for redirection and checking if the question is updated...")
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/manage_quiz"))
    time.sleep(1)

    page_source = driver.page_source
    if "When did WHO declare COVID-19 a pandemic?" in page_source:
        print("✅ Quiz question updated successfully!")
    else:
        print("❌ Quiz question not updated.")

    print("📍 Deleting the recently added quiz question...")
    delete_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Delete')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", delete_btn)
    delete_btn.click()

    print("📍 Waiting for deletion confirmation...")
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    Alert(driver).accept()

    print("📍 Waiting for page reload...")
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/manage_quiz"))
    time.sleep(1)

    print("📍 Checking if the question was deleted...")
    page_source = driver.page_source
    if "COVID-19" not in page_source:
        print("✅ Quiz question deleted successfully!")
    else:
        print("❌ Quiz question not deleted.")

except Exception as e:
    print(f"❌ Error during admin quiz automation: {e}")
    print(driver.page_source)

finally:
    time.sleep(5)
    driver.quit()
