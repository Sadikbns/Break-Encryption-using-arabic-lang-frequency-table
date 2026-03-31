# Arabic Letter Frequency Table Builder
# Scrapes Arabic news websites and builds a frequency table for cryptanalysis

import requests
from bs4 import BeautifulSoup
import re
import json
import os
from collections import OrderedDict

# ──────────────────────────────────────────────
# 1.1 - Define websites
# ──────────────────────────────────────────────

headers = {'User-Agent': 'Mozilla/5.0'}

sites = {
    # Gulf
    'aljazeera':     {'url': 'https://www.aljazeera.net'},
    'alarabiya':     {'url': 'https://www.alarabiya.net'},
    'skynews':       {'url': 'https://www.skynewsarabia.com'},
    'alhurra':       {'url': 'https://www.alhurra.com'},
    'france24':      {'url': 'https://www.france24.com/ar'},
    'dw_arabic':     {'url': 'https://www.dw.com/ar'},

    # International in Arabic
    'bbc_arabic':    {'url': 'https://www.bbc.com/arabic'},
    'rt_arabic':     {'url': 'https://arabic.rt.com'},
    'cnn_arabic':    {'url': 'https://arabic.cnn.com'},

    # Egypt
    'masrawy':       {'url': 'https://www.masrawy.com'},
    'youm7':         {'url': 'https://www.youm7.com'},

    # Saudi
    'sabq':          {'url': 'https://sabq.org'},
    'okaz':          {'url': 'https://www.okaz.com.sa'},
    'aleqtisadiya':  {'url': 'https://www.aleqt.com'},

    # Algeria
    'echorouk':      {'url': 'https://www.echoroukonline.com'},
    'ennahar DZ':    {'url': 'https://www.ennaharonline.com'},

    # Lebanon / Syria
    'annahar Leb':   {'url': 'https://www.annahar.com'},
    'asharqalawsat': {'url': 'https://aawsat.com'},
    'almodon':       {'url': 'https://www.almodon.com'},
}

CACHE_FILE = 'scraped_text.txt'
FORCE_RESCRAPE = False  # set to True when you want to re-scrape


# ──────────────────────────────────────────────
# 1.2 - Scrape websites and save to cache file
# ──────────────────────────────────────────────

def scrape_arabic_text(sites: dict, headers: dict) -> str:
    """
    Visits each site, extracts visible Arabic text from <p>, <h1>-<h3>,
    <span>, <a> tags, and returns the combined text.
    """
    all_text = []

    for name, info in sites.items():
        url = info['url']
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text from meaningful tags
            tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'a', 'li'])
            page_text = ' '.join(tag.get_text(separator=' ') for tag in tags)

            # Keep only Arabic characters and spaces (strip Latin, numbers, punctuation)
            arabic_only = re.sub(r'[^\u0600-\u06FF\s]', ' ', page_text)
            arabic_only = re.sub(r'\s+', ' ', arabic_only).strip()

            all_text.append(arabic_only)
            print(f"  ✓ {name}")

        except Exception as e:
            print(f"  ✗ {name}: {e}")

    return ' '.join(all_text)


def get_text(sites: dict, headers: dict, cache_file: str, force: bool) -> str:
    """
    Returns scraped text, using cache if available and force=False.
    """
    if not force and os.path.exists(cache_file):
        print(f"[INFO] Loading from cache: {cache_file}")
        with open(cache_file, 'r', encoding='utf-8') as f:
            return f.read()

    print("[INFO] Scraping websites...")
    text = scrape_arabic_text(sites, headers)

    with open(cache_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"[INFO] Saved to {cache_file} ({len(text):,} characters)")
    return text


# ──────────────────────────────────────────────
# 1.3 - Define Arabic alphabet dictionary
# ──────────────────────────────────────────────

def build_alphabet_count() -> dict:
    """
    Returns an OrderedDict of every Arabic letter (including variants
    and special characters) mapped to 0.
    Space is included as ' '.
    """
    alphabet_count = OrderedDict([
        # Core 28 letters
        ('ا', 0),  # Alef
        ('أ', 0),  # Alef with hamza above
        ('إ', 0),  # Alef with hamza below
        ('آ', 0),  # Alef with madda
        ('ء', 0),  # Hamza (standalone)
        ('ب', 0),  # Ba
        ('ت', 0),  # Ta
        ('ث', 0),  # Tha
        ('ج', 0),  # Jim
        ('ح', 0),  # Ha
        ('خ', 0),  # Kha
        ('د', 0),  # Dal
        ('ذ', 0),  # Dhal
        ('ر', 0),  # Ra
        ('ز', 0),  # Zain
        ('س', 0),  # Sin
        ('ش', 0),  # Shin
        ('ص', 0),  # Sad
        ('ض', 0),  # Dad
        ('ط', 0),  # Ta (emphatic)
        ('ظ', 0),  # Dha (emphatic)
        ('ع', 0),  # Ain
        ('غ', 0),  # Ghain
        ('ف', 0),  # Fa
        ('ق', 0),  # Qaf
        ('ك', 0),  # Kaf
        ('ل', 0),  # Lam
        ('م', 0),  # Mim
        ('ن', 0),  # Nun
        ('ه', 0),  # Ha
        ('و', 0),  # Waw
        ('ي', 0),  # Ya
        # Special / variant forms
        ('ة', 0),  # Ta marbuta
        ('ى', 0),  # Alef maqsura (dotless ya)
        ('ئ', 0),  # Ya with hamza
        ('ؤ', 0),  # Waw with hamza
        ('لا', 0), # Lam-Alef ligature (treated as digraph)
    ])
    return alphabet_count


# ──────────────────────────────────────────────
# 1.4 - Count letter occurrences
# ──────────────────────────────────────────────

def count_letters(text: str, alphabet_count: dict) -> dict:
    """
    Iterates over the text and counts occurrences of each tracked character.
    Digraphs (لا) are checked first before individual characters.
    """
    i = 0
    while i < len(text):
        # Check for digraph لا first
        if i + 1 < len(text) and text[i:i+2] == 'لا':
            alphabet_count['لا'] += 1
            i += 2
            continue
        char = text[i]
        if char in alphabet_count:
            alphabet_count[char] += 1
        i += 1
    return alphabet_count


# ──────────────────────────────────────────────
# 1.5 - Compute percentage frequency table
# ──────────────────────────────────────────────

def compute_frequency(alphabet_count: dict) -> dict:
    """
    Converts raw counts to percentage frequencies.
    Total = sum of all tracked character counts (including space).
    """
    total = sum(alphabet_count.values())
    if total == 0:
        return {k: 0.0 for k in alphabet_count}

    alphabet_percentage = OrderedDict(
        sorted(
            ((letter, round((count / total) * 100, 4)) for letter, count in alphabet_count.items()),
            key=lambda x: x[1],
            reverse=True
        )
    )
    return alphabet_percentage


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

if __name__ == '__main__':

    # Step 1.2 – get text
    text = get_text(sites, headers, CACHE_FILE, FORCE_RESCRAPE)
    print(f"[INFO] Total characters available: {len(text):,}")

    # Step 1.3 – build empty alphabet dict
    alphabet_count = build_alphabet_count()

    # Step 1.4 – fill counts
    alphabet_count = count_letters(text, alphabet_count)

    # Step 1.5 – compute percentages
    alphabet_percentage = compute_frequency(alphabet_count)

    # ── Display results ──────────────────────
    print("\n══════════════════════════════════════")
    print("  Arabic Letter Frequency Table")
    print("══════════════════════════════════════")
    print(f"  {'Letter':<8} {'Count':>10}   {'Freq %':>8}")
    print("──────────────────────────────────────")

    for letter, pct in alphabet_percentage.items():
        count = alphabet_count[letter]
        label = repr(letter) if letter == ' ' else letter
        print(f"  {label:<8} {count:>10,}   {pct:>7.4f}%")

    print("══════════════════════════════════════")
    total_chars = sum(alphabet_count.values())
    print(f"  Total tracked chars: {total_chars:,}")

    # ── Save frequency table to JSON ─────────
    output_json = 'arabic_freq_table.json'
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(alphabet_percentage, f, ensure_ascii=False, indent=2)
    print(f"\n[INFO] Frequency table saved to: {output_json}")