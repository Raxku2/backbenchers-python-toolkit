# 🕵️‍♂️ Repo Scanner

A modern, cyberpunk-styled terminal tool built with `PyGithub` and `Rich`. 

Easily extract detailed repository statistics, branch matrices, and commit data from GitHub using a stunning, high-tech terminal UI — right from your command line.

## 🧰 Features
✅ Extract global repository stats (Stars, Size, Contributors, Releases)

✅ Decrypt active branch matrices (Authors, Timestamps, SHAs)

✅ Beautiful cyberpunk/Matrix aesthetic utilizing `rich` tables and panels

✅ Smart input parser (accepts raw `user/repo` or full GitHub URLs)

✅ Auto-caching system remembers your last scanned databank

✅ Graceful error handling for API limits and missing data

✅ Secure environment variable token loading

<!-- ## 🖼️ Preview
**⚙️ Terminal-based UI Example**

```text
+-----------------------------------------------------------------------------+
| > TARGET DATABANK (user/repo) (Q : Quit) (P : Previous repo facebook/react) |
| > _                                                                         |
|                                                                             |
| ⠧ Establishing secure uplink to facebook/react...                           |
|                                                                             |
| ╭─────────────────────────────────────────────────────────────────────────╮ |
| │ /// GLOBAL REPOSITORY INTEL : FACEBOOK/REACT ///                        │ |
| │ DATABANK        METRIC                           VALUE                  │ |
| │ VITAL STATS     Stars (Reputation)             221,452                  │ |
| │                 Last Updated       2026-04-15 13:33:25                  │ |
| │ CODEBASE        Total Branches                      54                  │ |
| │                 Repository Size              310.42 MB                  │ |
| ╰─────────────────────────────────────────────────────────────────────────╯ |
|                                                                             |
| ⠧ Decrypting commit logs... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%   |
+-----------------------------------------------------------------------------+
``` -->

<!-- ## 🧑‍💻 Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/cyber-intel-scanner.git
cd cyber-intel-scanner
pip install -r requirements.txt
``` -->

## 🧩 Requirements
Make sure you have these packages installed:

```bash
pip install PyGithub python-dotenv rich
```

## 🔐 Configuration (Important)
This tool requires a GitHub Personal Access Token (PAT) to bypass strict API rate limits.
1. Generate a PAT on GitHub (Settings > Developer Settings > Personal Access Tokens).
2. Create a `.env` file in the root directory.
3. Add your token to the `.env` file:
```env
GITHUB_TOKEN=your_personal_access_token_here
```

## 🚀 Usage
Run the app directly using Python:

```bash
python main.py
```

**Steps:**
1. Enter the target repository (e.g., `facebook/react`, or paste a full URL).
2. Use `P` to quick-load the previously scanned repository from cache.
3. Use `Q` to abort the uplink.
4. Watch the terminal extract and render the data matrix!

## 🧠 Code Overview
```python
import os
from dotenv import load_dotenv
from github import Github, Auth
from rich.console import Console
from rich.table import Table
```

The program:
* Uses **Rich** for the cyberpunk TUI layout, progress bars, and custom hex themes.
* Uses **PyGithub** to interface with the GitHub REST API securely.
* Implements **Regex** to automatically sanitize user inputs.
* Uses local file caching (`./cache/repo`) to streamline repetitive queries.

## 📁 Project Structure
```text
cyber-intel-scanner/
├── main.py                # Main application code
├── .env                   # Secure token storage (Create this!)
├── requirements.txt       # Dependency list
├── README.md              # Documentation
└── cache/
    └── repo               # Auto-generated cache file
```

## 🧾 Example Requirements File
```text
PyGithub
python-dotenv
rich
```

## 🧱 Tech Stack
| Component | Description |
| :--- | :--- |
| **Python** | Core language |
| **Rich** | Colored terminal text, tables, and loading spinners |
| **PyGithub** | Official GitHub REST API wrapper |
| **python-dotenv** | Environment variable management |

## 🛡️ Error Handling
* `[red]ERROR: NO GITHUB_TOKEN DETECTED[/red]` → Missing `.env` file or token.
* `[red]CONNECTION TERMINATED: Not Found[/red]` → Invalid repository name or private repo without access.
* `[red]ERROR: Failed to create cache directory/file.[/red]` → Operating system permission issue.

## 💡 Future Improvements
* [ ] Add interactive prompt to select and view specific commits.
* [ ] Add visual commit history graphs.
* [ ] Export extracted intel to JSON or CSV formats.
* [ ] Integrate GitHub API GraphQL for faster bulk branch scanning.

## 🧑‍💻 Author
Developed by: **Pinaka**
💬 *"Extracting databanks, one matrix at a time."*
