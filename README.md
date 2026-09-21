# E-Commerce Web Scraper

A Python-based web scraping application developed as part of **SkillCraft Technology Internship – Task 4**.

The project extracts product information such as **product names, prices, and ratings** from online e-commerce websites and stores the extracted information in a structured **CSV file**.

The scraper uses multiple extraction techniques so that it can work with websites having different HTML structures and dynamically loaded content.

---

## 📌 Task Objective

> Create a program that extracts product information, such as names, prices, and ratings, from an online e-commerce website and stores the data in a structured format like a CSV file.

This project fulfills the task by:

* Accepting an e-commerce website URL from the user
* Sending a request to the website
* Extracting structured product information
* Extracting product information from HTML elements when structured data is unavailable
* Using Playwright for JavaScript-rendered pages when required
* Removing duplicate products
* Storing the final results in a CSV file

---

## 🛠️ Technologies Used

* **Python**
* **Requests** – Sending HTTP requests
* **BeautifulSoup** – Parsing HTML content
* **Playwright** – Handling JavaScript-rendered websites
* **CSV** – Storing extracted data
* **JSON** – Processing JSON-LD structured product data

---

## ✨ Features

* User enters the website URL at runtime
* Automatically adds `https://` if required
* Extracts product names
* Extracts product prices
* Extracts product ratings
* Supports JSON-LD structured product data
* Supports HTML-based product extraction
* Uses multiple CSS selectors
* Supports JavaScript-rendered content through Playwright
* Removes duplicate products
* Saves results automatically to `products.csv`
* Displays the first five extracted products in the terminal
* Handles scraping errors without immediately terminating the program

---

## 🔄 How the Scraper Works

The scraper uses a three-level extraction approach.

### 1. Structured Data Extraction

First, the program checks whether the website contains **JSON-LD structured data**.

```text
Website
   ↓
JSON-LD Product Data
   ↓
Product Name
Price
Rating
   ↓
CSV File
```

JSON-LD is useful because many websites provide product information in a structured format inside the HTML.

The program searches for:

```text
application/ld+json
```

and checks for product information such as:

```text
Product
ItemList
name
offers
aggregateRating
```

---

### 2. HTML Extraction

If structured product data is not available, the program searches the normal HTML structure.

```text
Website
   ↓
Requests
   ↓
BeautifulSoup
   ↓
HTML Elements
   ↓
CSS Selectors
   ↓
Product Data
   ↓
CSV File
```

The program searches for common elements and attributes related to:

* Product
* Product name
* Price
* Rating
* Title

Multiple CSS selectors are used because different websites use different HTML structures.

Examples include:

```text
.product-title
.product-name
[class*='price']
[class*='rating']
[data-testid*='product']
```

---

### 3. JavaScript-Rendered Content

Some websites generate product information using JavaScript after the initial page loads.

For these websites, normal `requests` scraping may not contain the required product information.

The scraper therefore uses **Playwright**.

```text
Website
   ↓
Playwright
   ↓
Browser loads JavaScript
   ↓
Rendered HTML
   ↓
BeautifulSoup
   ↓
Product Data
   ↓
CSV File
```

This allows the scraper to work with dynamically rendered pages that require a browser environment.

---

## 🧠 Scraping Strategy

The overall workflow is:

```text
                Enter Website URL
                       ↓
              Send HTTP Request
                       ↓
             ┌─────────────────┐
             │ JSON-LD present?│
             └────────┬────────┘
                      │
              Yes     │     No
               ↓      │      ↓
        Extract JSON-LD      Search HTML
               ↓               ↓
          Product Data    Product Data
               │               │
               └───────┬───────┘
                       ↓
                Products Found?
                  /         \
                Yes          No
                 ↓            ↓
             Save CSV    Launch Playwright
                              ↓
                       Render JavaScript
                              ↓
                       Extract HTML
                              ↓
                        Remove Duplicates
                              ↓
                         Save CSV
```

---

## 🌐 Websites Tested

The scraper was tested on three different web scraping/e-commerce demonstration websites.

### 1. Books to Scrape

Website:

https://books.toscrape.com/

This website provides a collection of books with information such as:

* Book name
* Price
* Availability
* Rating

It was used as the first test case for standard web scraping.

---

### 2. Web Scraping Demo

Website:

https://www.web-scraping.dev/

This website provides different web scraping scenarios and product-style data.

It was used as the second test case to verify that the scraper could handle a different website structure.

---

### 3. Scraping Sandbox

Website:

https://scrapingsandbox.com/

This website provides simulated e-commerce product data for scraping practice.

It was used as the third test case to demonstrate the scraper on another product-oriented website.

---

## 📊 Extracted Data

The scraper stores the following fields:

| Field        | Description                  |
| ------------ | ---------------------------- |
| Product Name | Name or title of the product |
| Price        | Product price                |
| Rating       | Product rating               |

The CSV file is generated with the following columns:

```text
Product Name, Price, Rating
```

---

## 📁 Output File

After successful scraping, the program automatically creates:

```text
products.csv
```

Example:

```csv
Product Name,Price,Rating
Product 1,$29.99,4.5
Product 2,$19.99,4.2
Product 3,$39.99,4.8
```

The actual values depend on the website being scraped.

---

## 💻 Installation

### Step 1 – Clone the Repository

Clone the repository using:

```bash
git clone https://github.com/YOUR-USERNAME/Task4-Ecommerce-Web-Scraper.git
```

Move into the project directory:

```bash
cd Task4-Ecommerce-Web-Scraper
```

---

### Step 2 – Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows Command Prompt:

```bash
venv\Scripts\activate
```

For PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

---

### Step 3 – Install Dependencies

Install the required Python libraries:

```bash
python -m pip install -r requirements.txt
```

If Playwright browsers have not been installed yet, run:

```bash
python -m playwright install chromium
```

---

## ▶️ Running the Program

Run:

```bash
python web_scraper.py
```

The program displays:

```text
============================================================
       E-COMMERCE WEB SCRAPER
============================================================

Enter the e-commerce website URL:
```

Enter a website URL, for example:

```text
https://books.toscrape.com/
```

The program then attempts to extract product information.

---

## 🖥️ Example Execution

Example terminal output:

```text
============================================================
       E-COMMERCE WEB SCRAPER
============================================================

Enter the e-commerce website URL:
https://books.toscrape.com/

[1/2] Trying standard HTML scraping...

Structured product data found.

============================================================
SCRAPING COMPLETED SUCCESSFULLY
============================================================

Products found: 20
Output file: products.csv

First 5 results:

Name   : A Light in the Attic
Price  : GBP 51.77
Rating : N/A
----------------------------------------
```

The exact output depends on the website and the information provided by that website.

---

## 📷 Screenshots

Screenshots of the project execution are included in the `screenshots` folder.

Suggested screenshots:

### Screenshot 1 – Books to Scrape

Shows the scraper extracting product information from Books to Scrape.

### Screenshot 2 – Web Scraping Demo

Shows the scraper working with a different website structure.

### Screenshot 3 – Scraping Sandbox

Shows the scraper extracting product information from the third test website.

### Screenshot 4 – CSV Output

Shows the generated `products.csv` file containing:

* Product Name
* Price
* Rating

---

## 📂 Project Structure

```text
Task4-Ecommerce-Web-Scraper/
│
├── web_scraper.py
│
├── products.csv
│
├── requirements.txt
│
├── .gitignore
│
├── README.md
│
└── screenshots/
    ├── 01_books_to_scrape.png
    ├── 02_web_scraping_dev.png
    ├── 03_scraping_sandbox.png
    └── 04_csv_output.png
```

---

## 📦 Requirements

The project uses the following Python libraries:

```text
requests
beautifulsoup4
playwright
urllib3
```

The complete dependency list is available in:

```text
requirements.txt
```

---

## 🔐 SSL Handling

The project includes SSL handling for websites that may use certificates that cannot be verified by the local environment.

The scraper uses:

```python
verify=False
```

for Requests and:

```python
ignore_https_errors=True
```

for Playwright.

This was required for testing certain demonstration websites with certificate issues.

For production scraping of trusted websites, SSL certificate verification should normally remain enabled.

---

## ⚠️ Limitations

This scraper is designed primarily for educational and demonstration purposes.

Different websites use different:

* HTML structures
* CSS classes
* Product schemas
* JavaScript frameworks
* APIs
* Anti-bot systems

Therefore, no generic scraper can reliably extract product information from every e-commerce website without website-specific selectors or API handling.

Some websites may also:

* Block automated requests
* Require authentication
* Use CAPTCHA
* Load products through APIs
* Require JavaScript rendering
* Change their HTML structure

---

## 🚀 Future Improvements

Possible improvements include:

* Automatic pagination
* Export to JSON and Excel
* Image URL extraction
* Product availability extraction
* Category extraction
* Product URL extraction
* Better website-specific selector detection
* Retry mechanisms
* Proxy support
* Database storage
* GUI interface
* Scheduled scraping
* API-based extraction
* Improved JavaScript handling

---

## 🎯 Learning Outcomes

Through this project, the following concepts were practiced:

* Python web scraping
* HTTP requests
* HTML parsing
* BeautifulSoup
* CSS selectors
* JSON-LD structured data
* CSV file handling
* Exception handling
* Data cleaning
* Duplicate removal
* Browser automation
* JavaScript-rendered webpages
* Playwright
* Virtual environments
* Python package management
* Git and GitHub

---

## 👩‍💻 Internship Task

**Internship:** SkillCraft Technology

**Task:** Task 4 – E-Commerce Web Scraping

**Language:** Python

**Output:** Structured CSV file containing extracted product information

---

## 📌 Conclusion

This project demonstrates how Python can be used to collect structured product information from web pages and store the extracted data in a CSV file.

The scraper combines **Requests, BeautifulSoup, JSON-LD extraction, HTML parsing, and Playwright** to handle different types of websites and dynamically rendered content.

The project was tested using multiple web scraping demonstration websites to verify the extraction workflow across different website structures.
