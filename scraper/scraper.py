from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

# Path to your ChromeDriver
webdriver_service = Service('/Users/saiteja/Downloads/chromedriver-mac-arm64/chromedriver')  # Update the path here

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=webdriver_service)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Update this with your MongoDB URI if required
db = client['results_database']  # Create/use a database
students = db['students']  # Create students collection
results = db['results']  # Create results collection

# URL of the main page with the form
url = 'https://www.nriitexamcell.com/autonomous/results.php'

# Open the page with the WebDriver
driver.get(url)

# Wait for the page to load
time.sleep(2)

# Extract notifications (if dynamically rendered, otherwise this will get static content)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Extract notifications
notifications = soup.find_all('td', class_='notification')

# Get regulation input from the user
reg = input("Enter regulation:").upper()

# Get academic year range input from the user
start_year = int(input("Enter starting academic year (e.g., 2022): "))
end_year = int(input("Enter ending academic year (e.g., 2026): "))

# Filter notifications based on the regulation and academic year range
def is_within_year_range(text, start_year, end_year):
    for year in range(start_year, end_year + 2):
        if str(year) in text:
            return True
    return False

# Filter notifications using both regulation and academic year range
filtered_results = list(filter(lambda notification: reg in notification.a.text.upper() and is_within_year_range(notification.a.text, start_year, end_year), notifications))

# Get roll number input from the user
roll = input("Enter Hall Ticket Number (roll):").strip()

# Check if student already exists in the database
student_exists = students.find_one({"roll": roll})  # Correct MongoDB query to check for an existing student

# Iterate through filtered results
for notification in filtered_results:
    # Construct the URL for the specific result page from the notification link
    result_url = 'https://www.nriitexamcell.com' + notification.a['href']
    
    # Open the result page using Selenium
    driver.get(result_url)
    
    # Find the roll number input field (adjust the name or ID based on the actual form)
    roll_input = driver.find_element(By.NAME, 'roll')  # Use the correct name or id of the input field
    roll_input.send_keys(roll)

    # Submit the form (adjust if the form uses a button or another method to submit)
    roll_input.send_keys(Keys.RETURN)

    # Wait for the result page to load
    time.sleep(2)

    # Get the page source after submission
    result_page_source = driver.page_source

    # Parse the page with BeautifulSoup
    result_soup = BeautifulSoup(result_page_source, 'html.parser')

    # Check if no records found
    no_record_message = result_soup.find('p', string="NO RECORDS FOUND FOR THIS NUMBER")
    if no_record_message:
        continue  # Skip to the next iteration if no records are found
    
    # If student doesn't exist, extract student info and store it
    if not student_exists:
        # Extract student name from the page
        student_name = ''
        name_element = result_soup.find('td', string="Name of the Student:")  # Find the cell with "Name of the Student"
        if name_element:
            # The name is in the next sibling <td>
            student_name = name_element.find_next_sibling('td').text.strip()  # Strip any extra spaces
            print(f"Student Name: {student_name}")

        # Create student data to store in the database
        student_data = {
            'name': student_name,
            'roll': roll,
            'start_year': start_year,
            'end_year': end_year
        }

        # Insert the new student data into the MongoDB collection
        students.insert_one(student_data)
        print("New student stored in DB.")
        student_exists = True  # Mark student as added


        #storing Results
        

# Close the browser when done
driver.quit()
