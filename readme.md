# Arabic Cryptanalysis Tool with Frequency Analysis

## 🎓 University Project

**Project Title:** Arabic Text Encryption and Cryptanalysis Using Frequency Analysis  
**Course:** Introduction to information security - Pr. Abdelkader Belkhir
**Student:** Bensadi Elsadik 232331351708
**Date:** March 2026

---

## 📋 Project Description

This project implements a complete Arabic language cryptography toolkit with a user-friendly graphical interface. It allows users to:

- Scrape real Arabic news websites to build a realistic letter frequency table
- Encrypt Arabic text using three classical ciphers: Caesar, Affine, and Monoalphabetic Substitution
- Attempt to break the encryption using frequency analysis (the most important feature)
- Test and compare different encryption methods

The tool is specifically designed for the Arabic language, handling its unique alphabet (including hamza, ta marbuta, lam-alef ligature, etc.).

## ✨ Features

### 1. Web Scraping Module
- Scrapes 15+ major Arabic news websites (Al Jazeera, BBC Arabic, Al Arabiya, Echorouk, etc.)
- Caches results to avoid repeated scraping
- Builds realistic frequency statistics based on modern Arabic text

### 2. Encryption Methods
- **Caesar Cipher** (shift cipher)
- **Affine Cipher** (linear transformation)
- **Monoalphabetic Substitution** (random permutation)

### 3. Frequency Analysis Attack
- Automatically maps the most frequent letters in ciphertext to the most frequent letters in Arabic
- Provides a strong baseline attack on substitution-based ciphers
- Works best with longer texts (> 200-300 characters)

### 4. Modern Tkinter GUI
- 4 clean tabs:
  - **🌐 Scrape News Websites**
  - **📊 Frequency Table**
  - **🔬 Test Encryption**
  - **🔐 Encrypt & Decrypt**
- Fully supports right-to-left Arabic text
- Responsive and user-friendly interface

## 📁 Project Files
frequency table project/
├── freq_table_builder.py          # Scrapes websites and builds frequency table
├── encryption_methods.py          # All encryption/decryption functions
├── main_ui.py                     # Main Tkinter graphical interface
├── arabic_freq_table.json         # Generated frequency table
├── scraped_text.txt               # Cached scraped text
└── README.md


## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- Required packages:
  ```bash
  pip install requests beautifulsoup4


# Submitted by: Bensadi Elsadik – Arabic Cryptanalysis Tool -USTHB-

Date: March 2026