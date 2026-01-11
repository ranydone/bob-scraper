# 🤖 COMPLETE AUTOMATION SETUP FOR BOB SCRAPER

## This guide provides 3 automation options:

---

## 📦 **OPTION 1: Python Script (Local/Server)**

### **Setup (One Time):**

```bash
# Install dependencies
pip install playwright pandas openpyxl
python -m playwright install chromium

# Download the script
# (use automated_bob_scraper.py)
```

### **Run Manually:**
```bash
python automated_bob_scraper.py
```

### **Run with Cron (Automated):**

```bash
# Edit crontab
crontab -e

# Add this line (runs every Monday at 9 AM):
0 9 * * 1 cd /path/to/scraper && python automated_bob_scraper.py >> scraper.log 2>&1

# Or every day at 8 AM:
0 8 * * * cd /path/to/scraper && python automated_bob_scraper.py >> scraper.log 2>&1

# Or every week on Sunday at 10 PM:
0 22 * * 0 cd /path/to/scraper && python automated_bob_scraper.py >> scraper.log 2>&1
```

**Cron Schedule Examples:**
- `0 9 * * 1` = Every Monday at 9:00 AM
- `0 8 * * *` = Every day at 8:00 AM
- `0 */6 * * *` = Every 6 hours
- `0 0 * * 0` = Every Sunday at midnight

---

## 🐳 **OPTION 2: Docker Container (Best for Servers)**

### **1. Create Dockerfile:**

```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install playwright pandas openpyxl

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps

# Set working directory
WORKDIR /app

# Copy scraper
COPY automated_bob_scraper.py .

# Run scraper
CMD ["python", "automated_bob_scraper.py"]
```

### **2. Build and Run:**

```bash
# Build image
docker build -t bob-scraper .

# Run once
docker run -v $(pwd)/output:/app bob-scraper

# Run with cron (add to host crontab)
0 9 * * 1 docker run -v /path/to/output:/app bob-scraper >> scraper.log 2>&1
```

---

## ☁️ **OPTION 3: GitHub Actions (Free Cloud Automation)**

### **Setup (Free, No Server Needed):**

**1. Create GitHub Repository**

**2. Add these files:**

**.github/workflows/scrape.yml:**
```yaml
name: BOB Scraper

on:
  schedule:
    # Runs every Monday at 9 AM UTC
    - cron: '0 9 * * 1'
  workflow_dispatch:  # Manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install playwright pandas openpyxl
        playwright install chromium
        playwright install-deps
    
    - name: Run scraper
      run: python automated_bob_scraper.py
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: scraper-results
        path: |
          bob_automated_scrape.json
          bob_automated_scrape.csv
          bob_automated_scrape.xlsx
          bob_scrape_summary.json
        retention-days: 90
    
    - name: Commit results (optional)
      run: |
        git config user.name "BOB Scraper Bot"
        git config user.email "scraper@example.com"
        git add bob_automated_scrape.*
        git commit -m "Update scraper results $(date)"
        git push
```

**Benefits:**
- ✅ Runs automatically on schedule
- ✅ Free (2,000 minutes/month)
- ✅ No server needed
- ✅ Results stored automatically
- ✅ Can trigger manually anytime

---

## 🚀 **OPTION 4: Google Colab with Scheduling**

### **Setup:**

**1. Create Google Colab Notebook:**

```python
# Cell 1: Install
!pip install -q playwright pandas openpyxl
!playwright install chromium

# Cell 2: Upload scraper code
# (paste automated_bob_scraper.py code)

# Cell 3: Run
import asyncio
asyncio.run(main())

# Cell 4: Download results
from google.colab import files
files.download('bob_automated_scrape.xlsx')
files.download('bob_automated_scrape.csv')
files.download('bob_automated_scrape.json')
```

**2. Schedule with Google Apps Script:**

```javascript
function runColabScraper() {
  // Open your Colab notebook
  var notebookUrl = 'YOUR_COLAB_NOTEBOOK_URL';
  
  // Use Colab API to run cells
  // (requires setup of Colab Pro with API access)
}

// Set trigger: Edit > Current project's triggers
// Add weekly trigger
```

---

## 📧 **EMAIL NOTIFICATIONS (Optional)**

### **Add to any automation:**

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email_notification(results_file):
    """Send email with results"""
    
    sender = "your-email@gmail.com"
    receiver = "recipient@example.com"
    password = "your-app-password"
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = f"BOB Scraper Results - {datetime.now().strftime('%Y-%m-%d')}"
    
    body = f"""
    BOB E-Auction Scraper Results
    
    Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Properties Found: {len(properties)}
    
    Files attached.
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach file
    with open(results_file, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={results_file}')
        msg.attach(part)
    
    # Send
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

# Add to scraper after save_results():
send_email_notification('bob_automated_scrape.xlsx')
```

---

## 💾 **DATABASE INTEGRATION**

### **Auto-import to MySQL/PostgreSQL:**

```python
import mysql.connector
# or: import psycopg2

def save_to_database(properties):
    """Save scraped data to database"""
    
    conn = mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="npa_properties"
    )
    
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bob_auctions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            borrower_name VARCHAR(255),
            branch VARCHAR(255),
            auction_date VARCHAR(50),
            zone VARCHAR(100),
            region VARCHAR(100),
            source VARCHAR(255),
            url TEXT,
            scraped_at DATETIME,
            UNIQUE KEY unique_auction (borrower_name, auction_date)
        )
    """)
    
    # Insert data (ignore duplicates)
    for prop in properties:
        cursor.execute("""
            INSERT IGNORE INTO bob_auctions 
            (borrower_name, branch, auction_date, zone, region, source, url, scraped_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            prop['borrower_name'],
            prop['branch'],
            prop['auction_date'],
            prop['zone'],
            prop['region'],
            prop['source'],
            prop['url'],
            prop['scraped_at']
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Saved {len(properties)} properties to database")

# Add to scraper after save_results():
save_to_database(self.properties)
```

---

## 📊 **RECOMMENDED SETUP**

### **For Personal Use:**
→ **Google Colab** (free, easy, no setup)

### **For Small Business:**
→ **GitHub Actions** (free, automated, cloud-based)

### **For Enterprise:**
→ **Docker + Cron** (reliable, scalable, self-hosted)

---

## ⏰ **SCHEDULING RECOMMENDATIONS**

**How often to scrape:**

- **Weekly**: Best for most use cases (every Monday)
  - Cron: `0 9 * * 1`
  
- **Daily**: If auctions change frequently
  - Cron: `0 8 * * *`
  
- **Twice/week**: Good balance
  - Cron: `0 9 * * 1,4` (Monday & Thursday)

**Don't scrape more than once per day** - unnecessary load on bank's servers.

---

## 🔧 **MONITORING & ALERTS**

### **Add health checks:**

```python
def send_alert_if_failed():
    """Send alert if scraping failed"""
    if len(properties) == 0:
        send_email(
            subject="⚠️ BOB Scraper Failed",
            body="No properties found. Check logs."
        )

def log_results():
    """Log to file for monitoring"""
    with open('scraper_history.log', 'a') as f:
        f.write(f"{datetime.now()}: Found {len(properties)} properties\n")
```

---

## 📝 **COMPLETE AUTOMATION WORKFLOW**

```
1. Scheduler triggers script
   ↓
2. Playwright scrapes website
   ↓
3. Data extracted & cleaned
   ↓
4. Files saved (JSON/CSV/Excel)
   ↓
5. Data imported to database (optional)
   ↓
6. Email sent with results (optional)
   ↓
7. Logs updated
   ↓
8. Done! (repeat weekly)
```

---

## 🎯 **WHICH OPTION TO CHOOSE?**

| Requirement | Best Option |
|-------------|-------------|
| Free, no server | GitHub Actions |
| Easy setup | Colab + manual |
| Most reliable | Docker + Cron |
| Quick start | Python script |
| Enterprise | Docker + K8s |

---

**Pick one option above and follow its setup guide!** 🚀
