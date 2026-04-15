from rich.traceback import install
from rich import print
install()
from textual.app import App
from textual.widgets import Header, Footer, Input, Button, Label,Static

from os.path import exists
from os import makedirs
from pyzipper import AESZipFile

class demoapp(App):
    TITLE = "Zip Extractor🔐"
    BINDINGS = [("q", "exitapp", "Close")]
    CSS = """
        Static {align: center middle}
    
        """

    def compose(self):
        yield Header(show_clock=True)
        yield Input(placeholder="Enter zip path ", id="zip_path")
        yield Input(placeholder="Enter output folder", id="ext_path")
        yield Input(placeholder="Enter Password", id="zip_passphrase")

        with Static():
            yield Button("Extract Zip..", id="extract_btn")
            yield Label("",id="status_box")
        yield Footer()

    def action_exitapp(self):
        self.exit()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "extract_btn":
            zip_path = self.query_one("#zip_path", Input).value
            ext_path = self.query_one("#ext_path", Input).value
            zip_passphrase = self.query_one("#zip_passphrase", Input).value

            status = self.query_one("#status_box", Label)

            zip_file = zip_path
            ext_dir = ext_path

            if not exists(zip_file):
                raise FileNotFoundError(f"{zip_file}Zip file not found")

            makedirs(ext_dir, exist_ok=True)

            password = zip_passphrase.encode('utf-8') if zip_passphrase else None 

            try:
                with AESZipFile(zip_file) as myzip:
                    myzip.extractall(path=ext_dir, pwd=password)
                status.update("[green]Extracted[/green]")
            except RuntimeError:
                if password: 
                    status.update("[red]Incorrect Password. Try again[/red]")
                else:
                    status.update("[red]Enter Password[/red]") 
            except :
                status.update("err")
        


demoapp().run()
