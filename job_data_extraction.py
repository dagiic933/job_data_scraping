from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv
from openpyxl import Workbook
from selenium.webdriver.firefox.options import Options

# Configure Firefox options
options = Options()
options.headless = False  # Set to True if you don't want the browser to be visible

# Create a new instance of the Firefox driver
driver = webdriver.Firefox(options=options)

# Navigate to the job listings page
driver.get('https://cvvp.nva.gov.lv/#/pub/vakances/saraksts#eyJvZmZzZXQiOjEyMDAsImxpbWl0IjoyNSwicGFnZVkiOjMwNn0%253D')

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table')))

# Function to extract job data from a row
def extract_job_data(row):
    columns = row.find_elements(By.TAG_NAME, 'td')
    return [column.text for column in columns]

# Extract job data from the current page
def extract_page_data():
    job_data = []
    rows = driver.find_elements(By.CSS_SELECTOR, '.table tbody tr')
    for row in rows:
        job_data.append(extract_job_data(row))
    return job_data

# Scroll to the bottom of the page
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract all job data
all_job_data = extract_page_data()

# Close the browser window
driver.quit()

# Save the data to CSV
with open('job_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Amats', 'Uzņēmums', 'Darba vietas adrese', 'Alga bruto', 'Aktuāla līdz'])
    csv_writer.writerows(all_job_data)

# Save the data to Excel
workbook = Workbook()
worksheet = workbook.active
worksheet.append(['Amats', 'Uzņēmums', 'Darba vietas adrese', 'Alga bruto', 'Aktuāla līdz'])
for job_row in all_job_data:
    worksheet.append(job_row)
workbook.save('job_data.xlsx')
