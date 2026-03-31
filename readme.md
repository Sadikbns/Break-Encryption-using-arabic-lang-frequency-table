# Arabic Cryptanalysis Tool with Frequency Analysis

## 🎓 University Project

**Project Title:** Arabic Text Encryption and Cryptanalysis Using Frequency Analysis  
**Course:** Introduction to information security - Pr. Abdelkader Belkhir
**Student:** Bensadi Elsadik 232331351708
**Date:** March 2026

---

## Project Description

This project implements a complete Arabic language cryptography toolkit with a user-friendly graphical interface. It allows users to:

- Scrape real Arabic news websites to build a realistic letter frequency table
- Encrypt Arabic text using three classical ciphers: Caesar, Affine, and Monoalphabetic Substitution
- Attempt to break the encryption using frequency analysis (the most important feature)
- Test and compare different encryption methods

The tool is specifically designed for the Arabic language, handling its unique alphabet (including hamza, ta marbuta, lam-alef ligature, etc.).

## Features

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
  - ** Scrape News Websites**
  - ** Frequency Table**
  - ** Test Encryption**
  - ** Encrypt & Decrypt**
- Fully supports right-to-left Arabic text
- Responsive and user-friendly interface

## Project Files
frequency table project/
├── freq_table_builder.py          # Scrapes websites and builds frequency table
├── encryption_methods.py          # All encryption/decryption functions
├── main_ui.py                     # Main Tkinter graphical interface
├── arabic_freq_table.json         # Generated frequency table
├── scraped_text.txt               # Cached scraped text
└── README.md


## How to Run

### Prerequisites
- Python 3.8 or higher
- Required packages:
  ```bash
  pip install requests beautifulsoup4

# Arabic Cryptanalysis Tool

## Step-by-step Instructions

### 1. Clone / Download all project files

### 2. First Time Setup
```bash
python freq_table_builder.py
```

This will scrape websites and create `arabic_freq_table.json`

### 3. Launch the Application
```bash
python main_ui.py
```

## Using the Tool

1. Go to the **Scrape News Websites** tab and click **Start Scraping**
2. Go to **Frequency Table** to see the statistics
3. Use the **Encrypt & Decrypt** tab to encrypt text and test the frequency attack
4. Use the **Test Encryption** tab to experiment with different methods

## Arabic Letter Frequency

The tool uses real-world data collected from major Arabic news outlets. The most frequent letters in Arabic are typically:
```
ا، ل، و، م، ي، ن، ر، ب، ت، س ...
```

## Technologies Used

- Python 3
- Tkinter - GUI framework
- BeautifulSoup4 - Web scraping
- Requests - HTTP client
- JSON - Data storage

## Learning Objectives Demonstrated

- Classical cryptography algorithms
- Frequency analysis cryptanalysis
- Web scraping and data collection
- Handling Unicode and right-to-left languages
- Building desktop GUI applications
- Modular programming and code organization

## Limitations

- Frequency analysis works best on monoalphabetic ciphers
- Very short texts (under 50 characters) give poor results
- Some websites may block scraping (cache helps avoid this)
- Does not implement advanced techniques like bigram/trigram analysis (can be added as future work)

## Future Improvements

- Add bigram and trigram frequency analysis
- Implement hill climbing or simulated annealing for better decryption
- Add support for saving/loading custom substitution keys
- Export results to PDF report

---

Submitted by: Sadik | University Project - Arabic Cryptanalysis Tool | March 2026

## Submitted by: Bensadi Elsadik – Arabic Cryptanalysis Tool -USTHB-

Date: March 2026