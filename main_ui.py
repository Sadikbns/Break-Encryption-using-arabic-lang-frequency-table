# main_ui.py
# Tkinter UI for Arabic Text Encryption/Decryption with Frequency Analysis

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from collections import OrderedDict
import os
import threading

# Import from your existing modules
from encryption_methods import (
    arabic_alphabet,
    cesar_encrypt, cesar_decrypt,
    affine_encrypt, affine_decrypt,
    substitution_encrypt, substitution_decrypt,
    arabic_substitution,
    N
)

# Import the scraping function from freq_table_builder
from freq_table_builder import scrape_arabic_text, sites, headers, get_text, CACHE_FILE

# Load frequency table
FREQ_TABLE_PATH = 'arabic_freq_table.json'


def load_freq_table():
    if not os.path.exists(FREQ_TABLE_PATH):
        return {}
    try:
        with open(FREQ_TABLE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


class ArabicCryptoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arabic Text Crypto Tool - Frequency Analysis")
        self.root.geometry("1250x850")
        self.root.configure(bg='#f0f0f0')

        self.freq_table = load_freq_table()
        self.lang_ranked = list(self.freq_table.keys()) if self.freq_table else []

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        self.create_notebook()

    def create_notebook(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tab 1: Scrape News Websites (NEW)
        self.tab_scrape = ttk.Frame(notebook)
        notebook.add(self.tab_scrape, text="🌐 Scrape News Websites")

        # Tab 2: Frequency Table
        self.tab_freq = ttk.Frame(notebook)
        notebook.add(self.tab_freq, text="📊 Frequency Table")

        # Tab 3: Test Encryption Methods
        self.tab_test = ttk.Frame(notebook)
        notebook.add(self.tab_test, text="🔬 Test Encryption")

        # Tab 4: Main Crypto Tool
        self.tab_main = ttk.Frame(notebook)
        notebook.add(self.tab_main, text="🔐 Encrypt & Decrypt")

        self.build_scrape_tab()
        self.build_freq_tab()
        self.build_test_tab()
        self.build_main_tab()

    # ====================== NEW TAB: Scrape News Websites ======================
    def build_scrape_tab(self):
        frame = ttk.Frame(self.tab_scrape, padding=15)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Scrape Arabic News Websites", 
                 font=('Arial', 16, 'bold')).pack(pady=(0, 15))

        # Instructions
        info = ttk.Label(frame, text="Click the button below to scrape multiple Arabic news websites and build/update the frequency table.\n"
                                    "This may take 20-60 seconds depending on your internet connection.",
                        wraplength=900, justify='center')
        info.pack(pady=10)

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=15)

        self.scrape_btn = ttk.Button(btn_frame, text="🚀 Start Scraping Websites", 
                                    command=self.start_scraping, style='Accent.TButton')
        self.scrape_btn.pack(side='left', padx=10)

        self.force_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(btn_frame, text="Force re-scrape (ignore cache)", 
                       variable=self.force_var).pack(side='left', padx=10)

        # Status and Progress
        self.status_var = tk.StringVar(value="Ready to scrape...")
        status_label = ttk.Label(frame, textvariable=self.status_var, font=('Arial', 10))
        status_label.pack(pady=8)

        # Scraped Text Output
        ttk.Label(frame, text="Scraped Raw Arabic Text (preview):", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(15,5))

        self.scraped_text_widget = scrolledtext.ScrolledText(frame, height=18, font=('Arial', 10))
        self.scraped_text_widget.pack(fill='both', expand=True, pady=5)

        # Info about sites
        sites_frame = ttk.LabelFrame(frame, text=f"News Websites to be scraped ({len(sites)} sites)", padding=8)
        sites_frame.pack(fill='x', pady=10)

        sites_text = ", ".join(sites.keys())
        ttk.Label(sites_frame, text=sites_text, wraplength=1100, justify='left', foreground='gray').pack()

    def start_scraping(self):
        self.scrape_btn.config(state='disabled')
        self.status_var.set("Scraping in progress... Please wait (this may take a while)")

        # Run scraping in a separate thread to keep UI responsive
        threading.Thread(target=self.run_scraping, daemon=True).start()

    def run_scraping(self):
        try:
            force = self.force_var.get()
            
            self.root.after(0, lambda: self.status_var.set("Connecting to news websites..."))

            # Use the existing get_text function
            text = get_text(sites, headers, CACHE_FILE, force)

            # Update UI from main thread
            self.root.after(0, lambda: self.finish_scraping(text))

        except Exception as e:
            self.root.after(0, lambda: self.scraping_error(str(e)))

    def finish_scraping(self, text):
        # Show preview of scraped text
        preview = text[:1500] + "..." if len(text) > 1500 else text
        self.scraped_text_widget.delete("1.0", tk.END)
        self.scraped_text_widget.insert(tk.END, preview)

        char_count = len(text)
        self.status_var.set(f"✅ Scraping completed successfully! Total characters: {char_count:,}")

        messagebox.showinfo("Success", 
            f"Scraping completed!\n\n"
            f"Total Arabic text collected: {char_count:,} characters\n"
            f"Cache saved to: {CACHE_FILE}\n\n"
            f"You can now go to the 'Frequency Table' tab to see updated frequencies.\n"
            f"Run freq_table_builder.py manually if you want to regenerate the .json file.")

        self.scrape_btn.config(state='normal')

    def scraping_error(self, error_msg):
        self.status_var.set("❌ Scraping failed")
        messagebox.showerror("Scraping Error", f"An error occurred during scraping:\n\n{error_msg}")
        self.scrape_btn.config(state='normal')

    # ====================== TAB: Frequency Table ======================
    def build_freq_tab(self):
        frame = ttk.Frame(self.tab_freq, padding=10)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Arabic Language Frequency Table", font=('Arial', 16, 'bold')).pack(pady=10)

        tree = ttk.Treeview(frame, columns=('Letter', 'Freq%'), show='headings', height=22)
        tree.heading('Letter', text='Letter')
        tree.heading('Freq%', text='Frequency %')
        tree.column('Letter', width=100, anchor='center')
        tree.column('Freq%', width=150, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for letter, pct in self.freq_table.items():
            tree.insert('', 'end', values=(letter, f"{pct:.4f}%"))

        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        ttk.Label(frame, text="Tip: Run the scraper and then freq_table_builder.py to update this table.", 
                 foreground='gray').pack(pady=5)

    # ====================== TAB: Test Encryption ======================
    def build_test_tab(self):
        frame = ttk.Frame(self.tab_test, padding=15)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Test Encryption/Decryption Methods", font=('Arial', 14, 'bold')).pack(pady=10)

        ttk.Label(frame, text="Enter Arabic Text:").pack(anchor='w')
        self.test_input = scrolledtext.ScrolledText(frame, height=8, font=('Arial', 11))
        self.test_input.pack(fill='x', pady=5)

        method_frame = ttk.Frame(frame)
        method_frame.pack(fill='x', pady=8)

        ttk.Label(method_frame, text="Method:").pack(side='left')
        self.test_method = tk.StringVar(value='cesar')
        for m in ['cesar', 'affine', 'substitution']:
            ttk.Radiobutton(method_frame, text=m.capitalize(), variable=self.test_method, value=m).pack(side='left', padx=12)

        param_frame = ttk.Frame(frame)
        param_frame.pack(fill='x', pady=5)

        ttk.Label(param_frame, text="Shift (Caesar):").grid(row=0, column=0, sticky='w')
        self.shift_var = tk.IntVar(value=7)
        ttk.Entry(param_frame, textvariable=self.shift_var, width=10).grid(row=0, column=1, padx=5)

        ttk.Label(param_frame, text="a (Affine):").grid(row=1, column=0, sticky='w')
        self.a_var = tk.IntVar(value=5)
        ttk.Entry(param_frame, textvariable=self.a_var, width=10).grid(row=1, column=1, padx=5)

        ttk.Label(param_frame, text="b (Affine):").grid(row=1, column=2, sticky='w', padx=(20,0))
        self.b_var = tk.IntVar(value=8)
        ttk.Entry(param_frame, textvariable=self.b_var, width=10).grid(row=1, column=3, padx=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=12)

        ttk.Button(btn_frame, text="Encrypt", command=self.test_encrypt).pack(side='left', padx=8)
        ttk.Button(btn_frame, text="Decrypt", command=self.test_decrypt).pack(side='left', padx=8)

        ttk.Label(frame, text="Result:").pack(anchor='w')
        self.test_output = scrolledtext.ScrolledText(frame, height=10, font=('Arial', 11))
        self.test_output.pack(fill='both', expand=True)

    def test_encrypt(self):
        text = self.test_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text")
            return

        method = self.test_method.get()
        try:
            if method == 'cesar':
                result = cesar_encrypt(text, self.shift_var.get())
            elif method == 'affine':
                result = affine_encrypt(text, self.a_var.get(), self.b_var.get())
            else:
                result = substitution_encrypt(text)

            self.test_output.delete("1.0", tk.END)
            self.test_output.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def test_decrypt(self):
        text = self.test_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text")
            return

        method = self.test_method.get()
        try:
            if method == 'cesar':
                result = cesar_decrypt(text, self.shift_var.get())
            elif method == 'affine':
                result = affine_decrypt(text, self.a_var.get(), self.b_var.get())
            else:
                result = substitution_decrypt(text)

            self.test_output.delete("1.0", tk.END)
            self.test_output.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ====================== TAB: Main Crypto Tool ======================
    def build_main_tab(self):
        frame = ttk.Frame(self.tab_main, padding=15)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Arabic Encryption + Frequency Analysis Attack", 
                 font=('Arial', 16, 'bold')).pack(pady=10)

        input_frame = ttk.LabelFrame(frame, text="Plaintext (minimum 30 characters recommended)", padding=10)
        input_frame.pack(fill='x', pady=8)

        self.plain_text = scrolledtext.ScrolledText(input_frame, height=8, font=('Arial', 12))
        self.plain_text.pack(fill='x')

        control_frame = ttk.Frame(frame)
        control_frame.pack(fill='x', pady=10)

        ttk.Label(control_frame, text="Encryption Method:").pack(side='left', padx=(0,10))
        self.enc_method = tk.StringVar(value='cesar')
        for m in ['cesar', 'affine', 'substitution']:
            ttk.Radiobutton(control_frame, text=m.capitalize(), variable=self.enc_method, value=m).pack(side='left', padx=10)

        ttk.Button(control_frame, text="Encrypt", command=self.encrypt_text).pack(side='right', padx=5)

        enc_frame = ttk.LabelFrame(frame, text="Encrypted Text", padding=10)
        enc_frame.pack(fill='x', pady=8)

        self.encrypted_text = scrolledtext.ScrolledText(enc_frame, height=6, font=('Arial', 12), fg='#d32f2f')
        self.encrypted_text.pack(fill='x')

        ttk.Button(frame, text="🔍 Decrypt Using Frequency Table", 
                  command=self.decrypt_using_freq).pack(pady=15)

        dec_frame = ttk.LabelFrame(frame, text="Decrypted Using Frequency Analysis", padding=10)
        dec_frame.pack(fill='both', expand=True)

        self.decrypted_text = scrolledtext.ScrolledText(dec_frame, height=10, font=('Arial', 12), fg='#2e7d32')
        self.decrypted_text.pack(fill='both', expand=True)

    def encrypt_text(self):
        plaintext = self.plain_text.get("1.0", tk.END).strip()
        if len(plaintext) < 30:
            messagebox.showwarning("Warning", "Please enter at least 30 characters of Arabic text for better results.")
            return

        method = self.enc_method.get()
        try:
            if method == 'cesar':
                encrypted = cesar_encrypt(plaintext, 7)
            elif method == 'affine':
                encrypted = affine_encrypt(plaintext, 5, 8)
            else:
                encrypted = substitution_encrypt(plaintext)

            self.encrypted_text.delete("1.0", tk.END)
            self.encrypted_text.insert(tk.END, encrypted)
            self.decrypted_text.delete("1.0", tk.END)

            messagebox.showinfo("Success", f"Text encrypted using {method} cipher!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt_using_freq(self):
        ciphertext = self.encrypted_text.get("1.0", tk.END).strip()
        if not ciphertext:
            messagebox.showwarning("Warning", "Please encrypt some text first.")
            return

        if not self.lang_ranked:
            messagebox.showerror("Error", "Frequency table is empty. Please scrape websites and generate the table first.")
            return

        try:
            # Count frequency in ciphertext
            cipher_count = {}
            for ch in ciphertext:
                if ch in arabic_alphabet:
                    cipher_count[ch] = cipher_count.get(ch, 0) + 1

            if not cipher_count:
                messagebox.showwarning("Warning", "No Arabic letters found in encrypted text.")
                return

            cipher_ranked = [ch for ch, _ in sorted(cipher_count.items(), key=lambda x: x[1], reverse=True)]

            # Create mapping
            mapping = {}
            for rank, cipher_char in enumerate(cipher_ranked):
                if rank < len(self.lang_ranked):
                    mapping[cipher_char] = self.lang_ranked[rank]

            # Apply mapping
            result = [mapping.get(ch, ch) for ch in ciphertext]
            decrypted = ''.join(result)

            self.decrypted_text.delete("1.0", tk.END)
            self.decrypted_text.insert(tk.END, decrypted)

            messagebox.showinfo("Frequency Attack", 
                              "Decryption using frequency analysis completed!\n\n"
                              "Accuracy depends on text length and language statistics.")

        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ArabicCryptoUI(root)
    root.mainloop()