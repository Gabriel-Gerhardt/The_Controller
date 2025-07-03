from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Static
from textual.reactive import reactive
from textual.events import Key
from pathlib import Path
from typing import cast
from rich.text import Text
import shutil


class FileManagerApp(App):
    CSS_PATH = None
    BINDINGS = [("q", "quit", "Sair"),
    ("2", "copy_desktop", "Copiar p/ Desktop"),
       ("3", "move", "Mover"),
       ("p", "put", "Put (Colar)"),
    ]

    current_path = reactive(Path.cwd())
    copy_buffer = reactive(None)
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield ListView(id="file_list")
        yield Static("", id="message_bar")
        yield Footer()

    def on_mount(self):
        self.load_files()
        self.query_one("#file_list", ListView).focus()

    def load_files(self):
        self.title = "Controller - Normal"
        list_view = self.query_one("#file_list", ListView)
        list_view.clear()

        for item in sorted(self.current_path.iterdir()):
            if item.name.startswith("."):  # ← Ignora ocultos
                continue
            label = item.name
            list_view.append(ListItem(Static(Text(label))))
        list_view.append(ListItem(Static(Text(".temp"))))

    def show_message(self, message: str):
        message_bar = self.query_one("#message_bar", Static)
        message_bar.update(message)

    async def on_key(self, event: Key):
        list_view = self.query_one("#file_list", ListView)

        if list_view.index is None or list_view.index < 0:
            return

        selected_item = list_view.children[list_view.index]
        label_widget = cast(Static, selected_item.children[0])
        text = cast(Text, label_widget.renderable)
        label = text.plain.rstrip("/")
        selected_path = self.current_path / label
        if event.key == "right":
            new_path = self.current_path / label
            if new_path.is_dir():
                self.current_path = new_path
                self.load_files()

        elif event.key == "left":
            if self.current_path.parent != self.current_path:
                self.current_path = self.current_path.parent
                self.load_files()

        if event.key == "2":
            selected_path = self.current_path / label
            destination = Path("/Users/gabrielgerhardt/Desktop") / label

            if destination.exists():
                self.show_message(f"[blue]Aviso:[/] O arquivo '{label}' já existe no diretório. Copia cancelada.")
                return

            if selected_path.is_dir():
                shutil.copytree(selected_path, destination)
            elif selected_path.is_file():
                shutil.copy(selected_path, destination)

        elif event.key == "3":
            self.copy_buffer = selected_path
            self.show_message(f"[green]Selecionado para copiar:[/] '{label}'")
        elif event.key == "p" and self.copy_buffer:
                destination = self.current_path / self.copy_buffer.name
                if destination.exists():
                    self.show_message(f"[blue]Aviso:[/] '{destination.name}' já existe aqui.")
                    return

                try:
                    if self.copy_buffer.is_dir():
                        shutil.copytree(self.copy_buffer, destination)
                    else:
                        shutil.copy(self.copy_buffer, destination)

                    self.show_message(f"[blue]Copiado:[/] '{self.copy_buffer.name}' → '{self.current_path}'")
                    self.load_files()
                except Exception as e:
                    self.show_message(f"[blue]Erro:[/] {e}")


if __name__ == "__main__":
    app = FileManagerApp()
    app.run()
