# SauceDemo QA Project

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green)
![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A QA automation project for testing the [SauceDemo](https://www.saucedemo.com) web application.
Includes a full test plan, written test cases, and automated tests using Python and Selenium.

---

## What is SauceDemo

SauceDemo is a demo e-commerce website used for practicing QA and test automation.
It has a login page, product listing, shopping cart, and checkout flow.

---

## What is inside this project

| File | What it is |
|---|---|
| `test_saucedemo.py` | Automated test cases written in Python using Selenium and Pytest |
| `SauceDemo_QA_Test_Plan.txt` | Full QA test plan covering all features |
| `SauceDemo_Test_Cases.txt` | 26 written test cases with steps and expected results |

---

## Tech stack

- Language: Python 3
- Automation: Selenium WebDriver
- Test runner: Pytest
- Browser: Chrome
- Testing type: Manual + Automation

---

## What I tested

- Login (valid, invalid, locked user, empty fields)
- Product listing (6 products, sorting, detail page)
- Shopping cart (add, remove, badge count)
- Checkout (full flow, validation errors, order summary)
- Logout (burger menu, redirect after logout)

Total: 27 automated test cases

---

## How to run the tests

**1. Clone the repo**
```bash
git clone https://github.com/taha09-qa/QA-project1
cd QA-project1
```

**2. Install the required libraries**
```bash
pip install selenium pytest
```

**3. Run all tests**
```bash
pytest test_saucedemo.py -v
```

---

## Test credentials used

| User | Password | Type |
|---|---|---|
| standard_user | secret_sauce | Valid user |
| locked_out_user | secret_sauce | Locked user |

---

## Author

**Taha** — Junior QA Engineer  
Manual Testing • Automation • Python • Selenium  
[GitHub](https://github.com/taha09-qa)
