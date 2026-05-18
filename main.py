
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from login import launch_login_window

from caesar import brute_force_caesar

from frequency import (
    calculate_frequency,
    suggest_mappings
)

from transposition import (
    detect_transposition,
    factor_text_length
)

from des_demo import compare_modes


# =================================================
# MAIN APPLICATION CLASS
# =================================================

class SecureCryptoSuite:

    def __init__(self, root):

        self.root = root

        self.root.title("Secure Cryptanalysis Tool Suite")

        self.root.geometry("1000x750")

        self.root.configure(bg="lightgray")

        self.create_tabs()


    # =================================================
    # CREATE TABS
    # =================================================

    def create_tabs(self):

        notebook = ttk.Notebook(self.root)

        notebook.pack(fill="both", expand=True)

        self.caesar_tab = ttk.Frame(notebook)
        self.frequency_tab = ttk.Frame(notebook)
        self.transposition_tab = ttk.Frame(notebook)
        self.des_tab = ttk.Frame(notebook)

        notebook.add(self.caesar_tab, text="Caesar Cracker")
        notebook.add(self.frequency_tab, text="Frequency Analysis")
        notebook.add(self.transposition_tab, text="Transposition Detector")
        notebook.add(self.des_tab, text="DES ECB vs CBC")

        self.build_caesar_tab()
        self.build_frequency_tab()
        self.build_transposition_tab()
        self.build_des_tab()


    # =================================================
    # CAESAR CRACKER TAB
    # =================================================

    def build_caesar_tab(self):

        title = tk.Label(
            self.caesar_tab,
            text="Caesar Cipher Cracker",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=10)

        tk.Label(
            self.caesar_tab,
            text="Enter Ciphertext:"
        ).pack()

        self.caesar_input = tk.Text(
            self.caesar_tab,
            width=90,
            height=8
        )

        self.caesar_input.pack(pady=10)

        crack_button = tk.Button(
            self.caesar_tab,
            text="Crack Cipher",
            command=self.run_caesar_attack,
            bg="black",
            fg="white",
            width=20
        )

        crack_button.pack(pady=10)

        self.caesar_output = tk.Text(
            self.caesar_tab,
            width=110,
            height=20
        )

        self.caesar_output.pack(pady=10)


    def run_caesar_attack(self):

        ciphertext = self.caesar_input.get("1.0", tk.END).strip()

        if not ciphertext:
            messagebox.showerror(
                "Error",
                "Please enter ciphertext"
            )
            return

        results = brute_force_caesar(ciphertext)

        self.caesar_output.delete("1.0", tk.END)

        self.caesar_output.insert(
            tk.END,
            "Top 3 Possible Solutions\n\n"
        )

        for result in results:

            self.caesar_output.insert(
                tk.END,
                f"Shift: {result['shift']}\n"
            )

            self.caesar_output.insert(
                tk.END,
                f"Chi-Squared Score: {result['score']}\n"
            )

            self.caesar_output.insert(
                tk.END,
                f"Confidence: {result['confidence']}%\n"
            )

            self.caesar_output.insert(
                tk.END,
                f"Plaintext:\n{result['text']}\n"
            )

            self.caesar_output.insert(
                tk.END,
                "-" * 60 + "\n"
            )


    # =================================================
    # FREQUENCY ANALYSIS TAB
    # =================================================

    def build_frequency_tab(self):

        title = tk.Label(
            self.frequency_tab,
            text="Substitution Cipher Analyzer",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=10)

        tk.Label(
            self.frequency_tab,
            text="Enter Ciphertext:"
        ).pack()

        self.frequency_input = tk.Text(
            self.frequency_tab,
            width=90,
            height=8
        )

        self.frequency_input.pack(pady=10)

        analyze_button = tk.Button(
            self.frequency_tab,
            text="Analyze Frequency",
            command=self.run_frequency_analysis,
            bg="darkblue",
            fg="white",
            width=20
        )

        analyze_button.pack(pady=10)

        self.frequency_output = tk.Text(
            self.frequency_tab,
            width=110,
            height=22
        )

        self.frequency_output.pack(pady=10)


    def run_frequency_analysis(self):

        ciphertext = self.frequency_input.get(
            "1.0",
            tk.END
        ).strip()

        if not ciphertext:
            messagebox.showerror(
                "Error",
                "Please enter ciphertext"
            )
            return

        frequencies = calculate_frequency(ciphertext)

        mappings = suggest_mappings(ciphertext)

        self.frequency_output.delete("1.0", tk.END)

        self.frequency_output.insert(
            tk.END,
            "LETTER FREQUENCIES\n\n"
        )

        for letter, value in sorted(frequencies.items()):

            self.frequency_output.insert(
                tk.END,
                f"{letter}: {value}%\n"
            )

        self.frequency_output.insert(
            tk.END,
            "\nSUGGESTED LETTER MAPPINGS\n\n"
        )

        for cipher_letter, english_letter in mappings.items():

            self.frequency_output.insert(
                tk.END,
                f"{cipher_letter} -> {english_letter}\n"
            )


    # =================================================
    # TRANSPOSITION TAB
    # =================================================

    def build_transposition_tab(self):

        title = tk.Label(
            self.transposition_tab,
            text="Transposition Cipher Detector",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=10)

        tk.Label(
            self.transposition_tab,
            text="Enter Ciphertext:"
        ).pack()

        self.transposition_input = tk.Text(
            self.transposition_tab,
            width=90,
            height=8
        )

        self.transposition_input.pack(pady=10)

        detect_button = tk.Button(
            self.transposition_tab,
            text="Detect Transposition",
            command=self.run_transposition_detection,
            bg="darkgreen",
            fg="white",
            width=25
        )

        detect_button.pack(pady=10)

        self.transposition_output = tk.Text(
            self.transposition_tab,
            width=110,
            height=22
        )

        self.transposition_output.pack(pady=10)


    def run_transposition_detection(self):

        ciphertext = self.transposition_input.get(
            "1.0",
            tk.END
        ).strip()

        if not ciphertext:
            messagebox.showerror(
                "Error",
                "Please enter ciphertext"
            )
            return

        detected, message = detect_transposition(ciphertext)

        self.transposition_output.delete("1.0", tk.END)

        self.transposition_output.insert(
            tk.END,
            message + "\n\n"
        )

        clean_length = len(
            ''.join(c for c in ciphertext if c.isalpha())
        )

        factors = factor_text_length(clean_length)

        self.transposition_output.insert(
            tk.END,
            f"Ciphertext Length: {clean_length}\n\n"
        )

        self.transposition_output.insert(
            tk.END,
            "Possible Matrix Sizes:\n\n"
        )

        for rows, cols in factors:

            self.transposition_output.insert(
                tk.END,
                f"{rows} x {cols}\n"
            )


    # =================================================
    # DES TAB
    # =================================================

    def build_des_tab(self):

        title = tk.Label(
            self.des_tab,
            text="DES ECB vs CBC Demonstration",
            font=("Arial", 16, "bold")
        )

        title.pack(pady=10)

        tk.Label(
            self.des_tab,
            text="Enter Plaintext:"
        ).pack()

        self.des_input = tk.Text(
            self.des_tab,
            width=90,
            height=8
        )

        self.des_input.pack(pady=10)

        tk.Label(
            self.des_tab,
            text="Enter DES Key:"
        ).pack()

        self.des_key = tk.Entry(
            self.des_tab,
            width=40
        )

        self.des_key.pack(pady=5)

        compare_button = tk.Button(
            self.des_tab,
            text="Compare ECB vs CBC",
            command=self.run_des_demo,
            bg="darkred",
            fg="white",
            width=25
        )

        compare_button.pack(pady=10)

        self.des_output = tk.Text(
            self.des_tab,
            width=110,
            height=24
        )

        self.des_output.pack(pady=10)


    def run_des_demo(self):

        plaintext = self.des_input.get(
            "1.0",
            tk.END
        ).strip()

        key = self.des_key.get().strip()

        if not plaintext or not key:

            messagebox.showerror(
                "Error",
                "Please enter plaintext and key"
            )

            return

        result = compare_modes(plaintext, key)

        self.des_output.delete("1.0", tk.END)

        self.des_output.insert(
            tk.END,
            "ECB MODE OUTPUT\n\n"
        )

        self.des_output.insert(
            tk.END,
            result["ECB"] + "\n\n"
        )

        self.des_output.insert(
            tk.END,
            "CBC MODE OUTPUT\n\n"
        )

        self.des_output.insert(
            tk.END,
            f"IV: {result['CBC_IV']}\n\n"
        )

        self.des_output.insert(
            tk.END,
            f"Ciphertext:\n{result['CBC_Ciphertext']}\n\n"
        )

        self.des_output.insert(
            tk.END,
            "SECURITY ANALYSIS\n\n"
        )

        self.des_output.insert(
            tk.END,
            "- ECB mode encrypts identical plaintext blocks identically.\n"
        )

        self.des_output.insert(
            tk.END,
            "- CBC mode uses an Initialization Vector (IV).\n"
        )

        self.des_output.insert(
            tk.END,
            "- CBC hides repeating patterns and is more secure.\n"
        )


# =================================================
# APPLICATION START
# =================================================

def launch_dashboard():

    root = tk.Tk()

    app = SecureCryptoSuite(root)

    root.mainloop()


if __name__ == "__main__":

    temp_root = tk.Tk()

    temp_root.withdraw()

    launch_login_window(launch_dashboard)

    temp_root.mainloop()