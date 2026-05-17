import os
import sys
import time
import requests
import argparse
import concurrent.futures
from threading import Lock
from bs4 import BeautifulSoup

# Initialize Thread Safety
db_lock = Lock()
print_lock = Lock()
found_results = []
student_name_holder = {"name": "Unknown Student", "registered": False}

def scrape_single_sheet(index, notification, roll, start_year, end_year):
    """Worker function to scrape a single result sheet."""
    sheet_title = notification.a.text.strip()
    result_url = 'https://www.nriitexamcell.com' + notification.a['href']
    
    try:
        payload = {
            'roll': roll,
            'submit': 'Get result'
        }
        res = requests.post(result_url, data=payload, timeout=8)
        res.raise_for_status()
    except Exception as e:
        with print_lock:
            print(f"   ⚠️ Connection error for '{sheet_title}': {e}")
        return

    result_soup = BeautifulSoup(res.text, 'html.parser')

    # Check if no records found
    no_record_message = result_soup.find('p', string="NO RECORDS FOUND FOR THIS NUMBER")
    if no_record_message or "NO RECORDS FOUND" in res.text:
        return

    # SUCCESS! Found a matching record for this student
    with print_lock:
        print(f"🎉 FOUND RECORDS in: {sheet_title}")
    
    # Store in list of found results
    found_results.append({
        "index": index,
        "semester": sheet_title,
        "url": result_url
    })

    # Thread-safe identification of student's name
    with db_lock:
        if not student_name_holder["registered"]:
            student_name = 'Unknown Student'
            name_element = result_soup.find('td', string="Name of the Student:")
            if name_element:
                student_name = name_element.find_next_sibling('td').text.strip()
            
            student_name_holder["name"] = student_name
            student_name_holder["registered"] = True
            with print_lock:
                print(f"👤 Student identified: {student_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standalone CLI CGPA & Semester Result Link Scraper")
    parser.add_argument("--roll", help="Hall Ticket Number (e.g. 20A91A1201)")
    parser.add_argument("--reg", help="Regulation (e.g. NRIA20)")
    parser.add_argument("--start", type=int, help="Starting academic year (e.g. 2022)")
    parser.add_argument("--end", type=int, help="Ending academic year (e.g. 2026)")
    parser.add_argument("--example", action="store_true", help="Run automatically with pre-configured example values (NRIA20, 2022, 2026, 22KN1A05D8)")
    args = parser.parse_args()

    print("=======================================================")
    print("🎓 NRIIT AUTONOMOUS SEMESTER RESULT CLI SCRAPER")
    print("=======================================================")

    # Resolve inputs (either from example flag or arguments/prompts)
    if args.example:
        print("💡 Running in Example Mode with default credentials...")
        reg = "NRIA20"
        start_year = 2022
        end_year = 2026
        roll = "22KN1A05D8"
    else:
        # Get regulation input
        reg = args.reg
        if not reg:
            reg = input("Enter regulation (e.g. NRIA20): ")
        reg = reg.upper().strip()

        # Get academic year range
        start_year = args.start
        if start_year is None:
            while True:
                try:
                    start_year = int(input("Enter starting academic year (e.g., 2022): "))
                    break
                except ValueError:
                    print("❌ Invalid input. Please enter a valid 4-digit year.")

        end_year = args.end
        if end_year is None:
            while True:
                try:
                    end_year = int(input("Enter ending academic year (e.g., 2026): "))
                    break
                except ValueError:
                    print("❌ Invalid input. Please enter a valid 4-digit year.")

        # Get roll number
        roll = args.roll
        if not roll:
            roll = input("Enter Hall Ticket Number (roll): ")
        roll = roll.upper().strip()

    # URL of the main page with the form list
    main_url = 'https://www.nriitexamcell.com/autonomous/results.php'

    print(f"\n🌐 Fetching announcement list from {main_url}...")
    try:
        response = requests.get(main_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Failed to reach exam cell server: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    notifications = soup.find_all('td', class_='notification')

    # Filter notifications based on the regulation and academic year range
    def is_within_year_range(text, start_year, end_year):
        for year in range(start_year, end_year + 2):
            if str(year) in text:
                return True
        return False

    filtered_results = list(filter(
        lambda n: reg in n.a.text.upper() and is_within_year_range(n.a.text, start_year, end_year), 
        notifications
    ))
    # Reverse the list so the oldest results sheets are ordered first
    filtered_results.reverse()

    print(f"\n🔎 Found {len(filtered_results)} result sheets matching {reg} in years {start_year}-{end_year}.")
    if not filtered_results:
        print("❌ No matching results found. Exiting.")
        sys.exit(0)

    # Execute in parallel using ThreadPoolExecutor
    max_workers = len(filtered_results)
    print(f"\n⚡ Scraping {len(filtered_results)} pages in parallel using {max_workers} threads...")
    start_scraping = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(scrape_single_sheet, idx, n, roll, start_year, end_year) 
            for idx, n in enumerate(filtered_results)
        ]
        concurrent.futures.wait(futures)

    duration = time.time() - start_scraping
    print(f"\n🎉 Parallel scraping finished in {duration:.2f} seconds!")

    # Print clean interactive summary report with clickable direct links
    if found_results:
        # Sort results so they appear in chronological order (oldest first)
        found_results.sort(key=lambda x: x["index"])
        
        print("\n=======================================================")
        print(f"📖 DIRECT SEMESTER LINKS FOR {roll} ({student_name_holder['name']})")
        print("=======================================================")
        for idx, item in enumerate(found_results, 1):
            print(f"{idx}. 🏫 {item['semester']}")
            print(f"   🔗 Direct Link: {item['url']}")
        print("=======================================================")
        print("\n💡 Tip: Cmd+Click (on Mac) or Ctrl+Click (on Windows/Linux) the links above to open them directly in your web browser!")
    else:
        print(f"\n❌ No records were found for roll number '{roll}' in any of the {len(filtered_results)} matching semesters.")
