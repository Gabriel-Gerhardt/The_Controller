from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Static
from textual.reactive import reactive
from textual.events import Key
from pathlib import Path
from typing import cast
from rich.text import Text


class FileManagerApp(App):
    CSS_PATH = None
    BINDINGS = [("q", "quit", "Sair")]

    current_path = reactive(Path.cwd())

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield ListView(id="file_list")
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


    async def on_key(self, event: Key):
        list_view = self.query_one("#file_list", ListView)

        if list_view.index is None or list_view.index < 0:
            return

        selected_item = list_view.children[list_view.index]
        label_widget = cast(Static, selected_item.children[0])
        text = cast(Text, label_widget.renderable)
        label = text.plain.rstrip("/")

        if event.key == "right":
            new_path = self.current_path / label
            if new_path.is_dir():
                self.current_path = new_path
                self.load_files()

        elif event.key == "left":
            if self.current_path.parent != self.current_path:
                self.current_path = self.current_path.parent
                self.load_files()


if __name__ == "__main__":
    app = FileManagerApp()
    app.run()
