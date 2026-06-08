Here's your README content — copy and paste it:

```markdown
# 📊 Data-Driven Test Pipeline — SauceDemo

A professional data-driven automated testing project built with 
Python, Selenium, and Pytest. Tests multiple users automatically 
by reading test data from a CSV file.

---

## 🛠️ Tools Used
- **Python** — core programming language
- **Selenium WebDriver** — browser automation
- **Pytest** — test framework
- **Pandas** — CSV file reading
- **pytest-html** — generates HTML test reports
- **Slack Webhook** — sends test results to Slack
- **WebDriverManager** — auto manages Chrome driver

---

## 🧪 What It Tests
| User | Expected |
|---|---|
| standard_user | ✅ Login should pass |
| locked_out_user | ❌ Should be blocked |
| wrong_user | ❌ Should be blocked |
| problem_user | ✅ Login should pass |
| performance_glitch_user | ✅ Login should pass |

---

## ⚙️ How It Works
1. Reads all users from `users.csv`
2. Opens Chrome browser automatically
3. Tests each user one by one
4. Reports pass or fail for each
5. Generates HTML report
6. Sends summary to Slack

---

## 🚀 How To Run
```bash
pip install selenium pytest pytest-html pandas webdriver-manager requests
py -m pytest test_data_driven.py -v --html=report.html
```

---

## 📁 Project Structure
```
data-driven-test-saucedemo/
├── test_data_driven.py   # main test file
├── users.csv             # test data
└── report.html           # generated after running
```

---

## 💡 Concepts Learned
- Data-driven testing with CSV
- Pytest parametrize decorator
- Selenium WebDriverWait
- HTML report generation
- Slack webhook integration
- Real QA industry technique

---

## 👨‍💻 Author
**Sarvnn**
Data-Driven QA Automation Project
