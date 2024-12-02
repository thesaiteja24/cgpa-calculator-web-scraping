# **CGPA Calculator**

The **CGPA Calculator** is a full-stack application that helps students calculate their **Cumulative Grade Point Average (CGPA)** by scraping student details from a college website. The application takes the **roll number** and **regulation** as input, scrapes the data, stores it in a database, and calculates and displays the CGPA and marks details.

---

## **Current Status**

- **Frontend**: React app is set up and ready with a clean UI built using **Tailwind CSS**.
- **Backend**: **Express** server is handling data requests, and the API for storing and fetching data is under development.
- **Scraper**: A Python scraper uses **BeautifulSoup** and **Selenium** to fetch student details from the college website based on the provided **roll number** and **regulation**.

---

## **Technologies Used**

- **Frontend**: React, Vite, Tailwind CSS
- **Backend**: Node.js, Express
- **Scraper**: Python, BeautifulSoup, Selenium
- **Database**: MongoDB
- **API**: RESTful API using Express to handle data from the frontend and database.

---

## **Folder Structure**

```plaintext
CGPA_Calculator/
├── frontend/              # React frontend
│   ├── public/            # Static files (index.html, images)
│   ├── src/               # Source code for the app
│   │   ├── assets/        # Assets like images
│   │   ├── components/    # Reusable React components
│   │   ├── App.css        # CSS styles
│   │   ├── App.jsx        # Main React component
│   │   ├── index.jsx      # React entry point
│   ├── package.json       # Frontend dependencies
│   ├── vite.config.js     # Vite configuration
├── backend/               # Express backend
│   ├── index.js           # Main server file
│   ├── package.json       # Backend dependencies
│   ├── package-lock.json  # Lock file for dependencies
│   ├── controllers/       # Controllers for handling requests
│   ├── models/            # Database models
│   ├── routes/            # API routes for CRUD operations
├── scraper/               # Python scraper
│   ├── scraper.py         # Script for data scraping
│   ├── requirements.txt   # Python dependencies
├── .gitignore             # Ignore unnecessary files in Git
├── README.md              # Project documentation
└── LICENSE                # License file
```

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/thesaiteja24/cgpa-calculator-web-scraping.git
cd cgpa-calculator-web-scraping
```

---

### **2. Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```
- Open your browser and navigate to `http://localhost:5173`.

---

### **3. Backend Setup**
```bash
cd backend
npm install
node index.js
```
- The Express server will start on `http://localhost:8080`.

---

### **4. Scraper Setup**
Ensure you have Python installed on your system.
```bash
cd scraper
pip install -r requirements.txt
python scraper.py
```
- The scraper fetches student details by using **roll number** and **regulation**, and stores them in the database.

---

## **Usage**

1. **Frontend**: Enter your **roll number** and **regulation** in the UI form. The system will scrape the student's details from the college website, and you will be able to view your **marks** and **CGPA** calculation instantly.
2. **Backend**: The Express backend handles the communication between the frontend and the database. It processes the scraped data and stores it for future reference.
3. **Scraper**: The Python scraper fetches the student’s academic data by making requests to the college website and parsing the HTML for the relevant details (such as marks, subjects, etc.).

---

## **Contributing**

Since this project is ongoing, contributions are welcome!  
1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature-name`).  
3. Commit your changes (`git commit -m "Add feature-name"`).  
4. Push to the branch (`git push origin feature-name`).  
5. Open a pull request.

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

## **Acknowledgments**

- Thanks to the creators of **React**, **Express**, and **Tailwind CSS** for their tools.
- Inspiration from various online tutorials and resources.

