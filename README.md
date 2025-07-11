# BreachCheck – CLI Tool for Data Breach Lookup

A secure and easy-to-use command-line interface (CLI) tool that checks whether a given email address has been exposed in any known data breaches using the HaveIBeenPwned (HIBP) API.

---

## 🚀 Features

- ✅ Check email addresses against known data breaches  
- 🔍 Detailed breach information including dates, domains, and compromised data  
- 📊 Clean, formatted table output  
- 🔒 Secure API key management  
- ⚡ Fast truncated responses option  
- 🛡️ Built-in security recommendations  

---

## 📋 Requirements

- Python 3.8 or higher  
- HaveIBeenPwned API key (get from [HIBP API Key](https://haveibeenpwned.com/API/Key))  
- Internet connection  

---

## 🔧 Installation

1. **Clone or download the project files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
````

3. **Set up your API key** (choose one method):

   **Method 1: Environment variable (recommended)**

   ```bash
   export HIBP_API_KEY="your_actual_api_key_here"
   ```

   **Method 2: Configuration file**

   * Edit `config/config.ini`
   * Replace `your_api_key_here` with your actual API key

---

## 🎯 Usage

### Basic email check:

```bash
python main.py check --email someone@example.com
```

### Fast check (truncated response):

```bash
python main.py check --email someone@example.com --truncate
```

---

## 📊 Sample Output

```
Checking breaches for: test@example.com  
Please wait...

⚠️  BREACHES FOUND for: test@example.com  
Total breaches: 2  
Verified breaches: 2  

Detailed Results:
================================================================================
+----------------+----------------+------------+----------------------+----------+--------+
| Breach Name    | Domain         | Date       | Data Compromised     | Affected | Status |
+================+================+============+======================+==========+========+
| LinkedIn       | linkedin.com   | 2016-05-18 | Emails, Passwords    | 164,611  | ✓      |
| Adobe          | adobe.com      | 2013-10-04 | Emails, Passwords    | 152,445  | ✓      |
+----------------+----------------+------------+----------------------+----------+--------+

Status Legend:
✓ = Verified breach  
🔒 = Sensitive breach  
🗄️ = Retired/historical breach  

🔒 Security Recommendations:
• Change passwords for all affected accounts immediately  
• Enable two-factor authentication (2FA)  
• Use a password manager with unique passwords  
• Monitor your accounts for suspicious activity  
• Check your credit report if financial data was leaked
```

---

## 📁 Project Structure

```
breachcheck/
├── main.py                     # Entry point and CLI interface
├── breachcheck/
│   ├── __init__.py             # Package initialization
│   ├── api.py                  # HIBP API client
│   ├── breaches.py             # Main breach checking logic
│   ├── display.py              # Output formatting and display
│   └── utils.py                # Utility functions
├── config/
│   └── config.ini              # Configuration file
├── .env                        # Environment variables (create this)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # License information
└── .gitignore                  # Git ignore rules
```

---

## ⚙️ Configuration

### Environment Variables

* `HIBP_API_KEY`: Your HaveIBeenPwned API key

### Config File Example (`config/config.ini`)

```ini
[HIBP]
API_KEY = your_api_key_here

[GENERAL]
DEFAULT_TRUNCATE = false
OUTPUT_FORMAT = table
```

---

## 🔐 Security Notes

* Never commit your API key to Git
* `.env` and `config.ini` are listed in `.gitignore`
* Tool prioritizes environment variables over config file
* Respects HIBP rate limits (1 request per 1.5 seconds)

---

## 🛠️ Error Handling

Handles common issues such as:

* ❌ Invalid email format
* ❌ Missing or invalid API key
* ❌ Network issues
* ❌ API rate limits
* ❌ API unavailability

---

## 🔍 API Reference

* **API Version**: v3
* **Base URL**: [https://haveibeenpwned.com/api/v3](https://haveibeenpwned.com/api/v3)
* **Rate Limit**: 1 request every 1.5 seconds
* **Docs**: [HIBP API Docs](https://haveibeenpwned.com/API/v3)
* **Authentication**: Required (API key)

---

## 🎨 Possible Enhancements

* [ ] Export results to JSON/CSV
* [ ] Bulk email check from file
* [ ] Password breach check
* [ ] Email masking
* [ ] Custom output formats
* [ ] Breach history tracker

---

## 📄 License

Licensed under the **MIT License**. See `LICENSE` for details.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a pull request

---

## ⚠️ Disclaimer

This tool is for educational and personal cybersecurity awareness use only. Use responsibly and lawfully.

---

## 🆘 Support

If you face issues:

* Validate your API key
* Check internet connection
* Ensure Python 3.8+ is installed
* Use `pip install -r requirements.txt`

---
