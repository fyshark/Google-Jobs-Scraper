# 🛠️ Google Jobs Scraper Tutorial (Berlin Softwareentwickler Jobs)

This repository provides a step-by-step guide to building a job scraper that pulls software job listings from **Google Jobs** using [SerpAPI](https://serpapi.com/).

It’s designed to help developers learn how to:
- Use SerpAPI to scrape job listings
- Parse localized time formats (e.g. German/English date strings)
- Export results to CSV using Python
- Filter and sort job listings using `pandas`

> 🚫 This project **does not include** a working script or API key to avoid using personal API credits. You are encouraged to implement and test it with your own credentials.

---

## 📦 What You’ll Learn

- How to search Google Jobs via API
- How to handle pagination with `next_page_token`
- How to parse both German and English "posted time"
- How to export top N job results to a CSV file

---

## 🔐 Get a SerpAPI Key

1. Go to [https://serpapi.com](https://serpapi.com)
2. Sign up for a free account
3. Copy your **API Key** from the dashboard

---

## 📁 Project Structure (suggested)
### job-scraper-tutorial/
### ├── job_scraper.py
### ├── .env
### ├── .gitignore
### ├── requirements.txt
### └── README.md
