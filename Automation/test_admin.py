import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

# Set up Edge driver
service = Service(executable_path=r"C:\edgedriver\msedgedriver.exe")
driver = webdriver.Edge(service=service)

# Open the Flask app login page
driver.get("http://127.0.0.1:5000/login")
time.sleep(2)

# Fill in the admin login form
driver.find_element(By.NAME, "username").send_keys("admin123")
driver.find_element(By.NAME, "password").send_keys("adminpass")
time.sleep(2)

# Click the login button
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(5)  # Wait to observe login result

# Close the browser
driver.quit()
