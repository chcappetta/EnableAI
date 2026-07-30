from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, Static, Button, ScrollView
from textual.reactive import reactive

import os
from openrouter import OpenRouter
import json
from memory import load_history, save_history
from auth import load_users, save_users, hash_password, verify_password

# Try to import the tools registry; fall back to empty dict if not available.
try:
    from tools.registry import TOOLS
except Exception:
    TOOLS = {}


class MessageBubble(Static):
    def __init__(self, role: str, content: str) -> None:
        super().__init__()
        self.role = role
        self.content = content

    def render(self) -> str:
        if self.role == "user":
            return f"You: {self.content}"
        elif self.role == "assistant":
            return f"AI: {self.content}"
        else:
            return f"*{self.content}*"


class EnableAIApp(App):
    CSS_PATH = None
    BINDINGS = [("ctrl+c", "quit", "Quit")]

    username = reactive(None)
    ai_name = reactive("Ruby")
    messages = reactive([])

    def __init__(self):
        super().__init__()
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            self.client = None
        else:
            self.client = OpenRouter(api_key)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container():
            yield Static("EnableAI — Textual TUI", id="title")
            yield Static("Enter a username and press Enter to begin (or type ':demo' to continue as demo).", id="subtitle")
            yield Input(placeholder="username", id="username_input")
            yield ScrollView(id="chat_scroll", name="chat")
            yield Input(placeholder="Type a message and press Enter", id="message_input")
            with Vertical():
                yield Button("Save conversation", id="save_btn")
                yield Button("Quit", id="quit_btn")
        yield Footer()

    async def on_mount(self) -> None:
        self.chat = self.query_one("#chat_scroll", ScrollView)
        self.user_input = self.query_one("#message_input", Input)
        self.username_input = self.query_one("#username_input", Input)
        self.save_btn = self.query_one("#save_btn", Button)
        self.quit_btn = self.query_one("#quit_btn", Button)

        # Focus username initially
        await self.username_input.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        widget = event.input
        if widget.id == "username_input":
            value = event.value.strip()
            if not value:
                return
            if value == ":demo":
                self.username = "demo"
            else:
                self.username = value
            # try to load history
            try:
                self.messages = load_history(self.username, self.ai_name)
            except Exception:
                # start with system message
                self.messages = [{"role": "system", "content": f"You are a helpful AI assistant named {self.ai_name}."}]
            await self.refresh_chat()
            await self.user_input.focus()
        elif widget.id == "message_input":
            if not self.username:
                await self.post_message("system", "Please enter username first in the username input.")
                return
            prompt = event.value.strip()
            if not prompt:
                return

            # Check for tool commands (commands start with '/')
            if prompt.startswith("/"):
                parts = prompt.split(maxsplit=1)
                cmd = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                if cmd in TOOLS:
                    try:
                        result = TOOLS[cmd](self.ai_name, self.username, args)
                        # Ensure result is a string
                        if result is None:
                            result = f"{self.ai_name}: Tool returned no result."
                        else:
                            result = str(result)
                    except Exception as e:
                        result = f"{self.ai_name}: Tool error: {e}"
                    await self.post_message("assistant", result)
                    self.query_one("#message_input", Input).value = ""
                    return

            # handle built-in commands as fallback
            if prompt.lower() == "/quit":
                await self.action_quit()
                return
            if prompt.lower() == "/help":
                await self.post_message("system", "Available commands: /help, /quit, /save, plus any /tools if available")
                self.query_one("#message_input", Input).value = ""
                return
            if prompt.lower() == "/save":
                save_history(self.username, self.messages)
                await self.post_message("system", "Conversation saved.")
                self.query_one("#message_input", Input).value = ""
                return

            # append user message
            self.messages.append({"role": "user", "content": prompt})
            await self.refresh_chat()
            self.query_one("#message_input", Input).value = ""
            # call AI
            await self.post_message("assistant", "Thinking...")
            await self.refresh_chat()
            # remove the Thinking placeholder and replace with real output
            try:
                if not self.client:
                    raise RuntimeError("OPENROUTER_API_KEY not set in environment")
                output = self.ai_response(self.client, self.messages)
            except Exception as e:
                output = f"Sorry, AI is unavailable: {e}. Other features still work."
            # replace last assistant message
            for i in range(len(self.messages)-1, -1, -1):
                if self.messages[i]["role"] == "assistant":
                    self.messages[i]["content"] = output
                    break
            else:
                self.messages.append({"role":"assistant","content":output})
            await self.refresh_chat()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "save_btn":
            if not self.username:
                await self.post_message("system", "Enter username before saving.")
                return
            save_history(self.username, self.messages)
            await self.post_message("system", "Saved conversation.")
        elif btn_id == "quit_btn":
            await self.action_quit()

    async def post_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        await self.refresh_chat()

    async def refresh_chat(self) -> None:
        self.chat.clear()
        for m in self.messages:
            bubble = MessageBubble(m.get("role"), m.get("content"))
            await self.chat.mount(bubble)
        # scroll to end
        await self.chat.scroll_end(animate=False)

    def ai_response(self, client, messages):
        # synchronous call to OpenRouter client to keep example simple
        response = client.chat.send(
            model="poolside/laguna-m.1:free",
            messages=messages
        )
        output = response.choices[0].message.content
        return output


if __name__ == "__main__":
    EnableAIApp().run()
