from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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
        EC.presence_of_element_located((By.LINK_TEXT, "Manage Facts"))
    )

    print("📍 Navigating to 'Manage Facts'...")
    driver.find_element(By.LINK_TEXT, "Manage Facts").click()

    print("📍 Waiting for 'Add New Fact' button to be clickable...")
    add_fact_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add New Fact"))
    )

    print("📍 Clicking 'Add New Fact' button...")
    add_fact_btn.click()

    # Adding a new fact
    print("📍 Filling in 'Add Fact' form...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    ).send_keys("Discovery of Electricity")

    driver.find_element(By.NAME, "description").send_keys(
        "Electricity was discovered in the 18th century by Benjamin Franklin."
    )

    print("📍 Submitting the new fact...")
    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Add Fact')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(1)
    submit_btn.click()

    # Verifying the fact was added
    print("📍 Waiting for redirection and verifying if the fact is added...")
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/manage_facts"))
    time.sleep(1)

    page_source = driver.page_source
    if "Discovery of Electricity" in page_source:
        print("✅ Fact added successfully!")
    else:
        print("❌ Fact not found after submission.")

    # Editing a fact
    print("📍 Clicking 'Edit' on the first fact...")
    edit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Edit')]"))
    )
    edit_btn.click()

    print("📍 Editing the fact...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    ).clear()  # Clearing the title
    driver.find_element(By.NAME, "title").send_keys("Invention of Electricity")

    driver.find_element(By.NAME, "description").clear()  # Clearing the description
    driver.find_element(By.NAME, "description").send_keys(
        "Electricity was invented by Alessandro Volta."
    )

    print("📍 Submitting the edited fact...")
    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Update Fact')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(1)
    submit_btn.click()

    # Verifying the fact was edited
    print("📍 Waiting for redirection and verifying the edit...")
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/manage_facts"))
    time.sleep(1)

    page_source = driver.page_source
    if "Invention of Electricity" in page_source:
        print("✅ Fact updated successfully!")
    else:
        print("❌ Fact not found after update.")

    # Deleting a fact
    print("📍 Deleting the fact...")
    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Delete')]"))
    )
    delete_btn.click()

    print("📍 Confirming the deletion...")
    WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )
    alert = driver.switch_to.alert
    alert.accept() 

    print("📍 Waiting for redirection and verifying the fact was deleted...")
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/manage_facts"))
    time.sleep(1)

    page_source = driver.page_source
    if "Invention of Electricity" not in page_source:
        print("✅ Fact deleted successfully!")
    else:
        print("❌ Fact still present after deletion.")

except Exception as e:
    print(f"❌ Error during admin fact automation: {e}")
    print(driver.page_source) 

finally:
    time.sleep(5)
    driver.quit()
