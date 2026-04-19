import pyperclip
from app.strganogtapher.zerowidth import ZeroWidthSteganographer, Fernet
from dotenv import load_dotenv
from os import getenv
from rich.console import Console
from rich.prompt import Prompt
from rich import print

console = Console()
clear = console.clear

Prompt.prompt_suffix = " "
input = Prompt.ask

load_dotenv()

if __name__ == "__main__":
    clear()
    print("[bold green]=== [italic]Zero-Width Steganographer[/] ===[/]")

    # master_key = Fernet.generate_key()
    # print(f"[!] Your Encryption Key (Save this in "SEC_KEY"!): {master_key.decode()}")
    stego = ZeroWidthSteganographer(getenv("SEC_KEY"))

    while True:
        print("\n1. Hide a message [magenta](Copy to Clipboard)[/]")
        print("2. Reveal a message [magenta](Read from Clipboard)[/]")
        print("3. [red]Exit[/]")
        choice = input(
            "[yellow]> [bold italic]Select an option[/][/]",
            choices=["1", "2", "3"],
            default="3",
        )

        if choice == "1":
            clear()
            secret = input("[cyan]> [green]Enter the secret message:[/]\n>[/]")
            clear()
            cover = input(
                "[cyan]> [green]Enter the public cover text [magenta]('Enter' for copy from clipboard)[/]:[/]\n>[/]"
            )
            clear()

            if cover == "":
                cover = pyperclip.paste()

            result = stego.hide(secret, cover)
            pyperclip.copy(result)

            print(
                "\n[green][bold][+] Success![/bold] The cover text containing your encrypted, invisible message has been copied to your clipboard.[/green]"
            )
            print(f"[cyan]> [green]Preview of text \n[/]>[/] [bold yellow]{result}[/]")
            if (
                input("\n\n> 'ENTER' to Continiue [magenta](q : Quit)[/]\n>").lower()
                == "q"
            ):
                clear()
                break
            else:
                clear()
                continue

        elif choice == "2":
            clear()

            print("\nReading from clipboard...")
            clipboard_data = pyperclip.paste()
            clear()
            revealed_secret = stego.reveal(clipboard_data)
            print(
                f">[bold green][+] Hidden Message Revealed[/]\n[cyan]>[/] [bold white]{revealed_secret}[/]"
            )
            if (
                input("\n\n> 'ENTER' to Continiue [magenta](q : Quit)[/]\n>").lower()
                == "q"
            ):
                clear()
                break
            else:
                clear()
                continue

        elif choice == "3":
            clear()
            break
        else:
            print("Invalid choice.")
