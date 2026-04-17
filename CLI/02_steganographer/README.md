<div align="center">

# 🕵️‍♂️ Zero-Width Steganographer

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)]()
[![Cryptography](https://img.shields.io/badge/Cryptography-AES--128-red?style=for-the-badge&logo=letsencrypt&logoColor=white)]()
[![CLI](https://img.shields.io/badge/UI-Rich--CLI-magenta?style=for-the-badge&logo=windows-terminal&logoColor=white)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)]()

**Hide encrypted, secret payloads in plain sight using invisible Unicode characters.**

</div>

---

## ⚡ The Concept

The Zero-Width Steganographer acts as an invisible ink injector for the modern web. It takes your secret message, mathematically encrypts it with a master key, converts that encrypted string into binary, and translates that binary into **Zero-Width Unicode Characters**. 

These characters are completely invisible in standard text editors, messaging apps, and websites. You inject them into a normal "cover text" (like a harmless greeting), and only someone with this script—and your exact encryption key—can extract and decrypt the secret inside.

---

## 📂 Project Architecture

```text
.
├── app/
│   ├── main.py                 # Interactive Rich CLI interface
│   └── strganogtapher/         # Core engine
│       ├── characters.py       # Zero-width Unicode definitions
│       └── zerowidth.py        # Cryptography & Steganography logic
├── .env                        # Local environment variables (You create this)
└── requirements.txt            # Project dependencies
````

-----

## 🚀 Getting Started

### 1\. Installation

It is highly recommended to run this inside a virtual environment. Navigate to the project root and install the dependencies:

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv .package
source .package/bin/activate  # On Windows: .package\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Note:** Your `requirements.txt` should include `pyperclip`, `cryptography`, `python-dotenv`, and `rich`.

### 2\. Generating Your Master Key

Before you can hide or reveal messages, you need a highly secure, mathematically random master key.

1.  Open `app/main.py`.
2.  Locate the `__main__` block (around line 20).
3.  **Uncomment** these two lines temporarily:
    ```python
    master_key = Fernet.generate_key()
    print(f"[!] Your Encryption Key (Save this in SEC_KEY!): {master_key.decode()}")
    ```
4.  Run the script: `python -m app.main`
5.  Copy the generated key from your terminal output.
6.  **Comment those lines back out.**

### 3\. Securing the Key (`.env`)

Create a `.env` file in the root of your project `~/D/C/Project/` and paste your key inside it:

```env
SEC_KEY=your_generated_base64_key_here=
```

-----

## 🎮 Usage

Run the application as a module from the root directory to ensure imports resolve correctly:

```bash
python -m app.main
```

### The Interface

The CLI utilizes `rich` for a beautiful, colorful terminal experience:

  * **Option 1 (Hide):** Type your secret, type a cover text (or press \<kbd\>Enter\</kbd\> to use whatever is currently on your clipboard), and the script will automatically copy the infected cover text back to your clipboard.
  * **Option 2 (Reveal):** Copy an infected text block to your clipboard from anywhere (Discord, Email, a text file) and select Option 2. The script will rip the invisible characters out, decrypt them, and display the secret.

-----

## 🧠 Under the Hood

### 🔒 The Encryption Process (Hiding)

| Phase | Action | Result |
| :--- | :--- | :--- |
| **1. AES Encryption** | Secures the raw text using `cryptography.fernet` | `Secret` ➔ `gAAAAABk...` |
| **2. Binary Translation** | Converts the AES string into raw machine code | `gAAAA...` ➔ `01100111...` |
| **3. Steganography** | Replaces bits with invisible unicode (`U+200B`, `U+200C`) | `0110...` ➔ `[Invisible Block]` |
| **4. Injection** | Splices the block right after the first character of cover text | `Hello` ➔ `H[Invisible]ello` |

### 🔓 The Decryption Process (Revealing)

| Phase | Action | Result |
| :--- | :--- | :--- |
| **1. Extraction** | Scans clipboard for Zero-Width Characters until the `DELIM` marker | `H[Invisible]ello` ➔ `[Invisible]` |
| **2. Binary Reversal** | Converts Unicode back to bits (`0` and `1`) | `[Invisible]` ➔ `01100111...` |
| **3. Text Reversal** | Converts the binary bits back to standard text | `0110...` ➔ `gAAAAABk...` |
| **4. AES Decryption** | Uses your `.env` `SEC_KEY` to unlock the Fernet cipher | `gAAAA...` ➔ `Secret` |

-----

\<div align="center"\>
\<i\>Operate quietly. Leave no trace.\</i\>
\</div\>

