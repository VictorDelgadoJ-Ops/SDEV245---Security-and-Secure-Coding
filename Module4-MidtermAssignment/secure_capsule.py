"""Integrity Capsule: an educational message and file protection workflow."""

from __future__ import annotations

import base64
import getpass
import hashlib
import hmac
import json
import secrets
import sys
import tkinter as tk
from datetime import datetime, timezone
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from cryptography.fernet import Fernet, InvalidToken


PBKDF2_ROUNDS = 120_000
CAPSULE_VERSION = 1
USERS: dict[str, dict[str, str]] = {
	"admin": {"role": "admin", "password_hash": ""},
	"student": {"role": "student", "password_hash": ""},
}


def password_digest(password: str, salt: bytes) -> str:
	digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS)
	return f"{salt.hex()}${digest.hex()}"


def create_demo_users() -> None:
	for username, password in (("admin", "Admin123!"), ("student", "Student123!")):
		salt = secrets.token_bytes(16)
		USERS[username]["password_hash"] = password_digest(password, salt)


def authenticate(username: str, password: str) -> str | None:
	account = USERS.get(username)
	if account is None:
		return None
	salt_hex, expected_hex = account["password_hash"].split("$")
	actual_hex = password_digest(password, bytes.fromhex(salt_hex)).split("$")[1]
	return account["role"] if hmac.compare_digest(actual_hex, expected_hex) else None


def sha256_bytes(data: bytes) -> str:
	return hashlib.sha256(data).hexdigest()


def make_capsule(payload: bytes, source_name: str, source_type: str) -> tuple[bytes, str]:
	"""Encrypt a self-describing package and return its token and key."""
	key = Fernet.generate_key()
	capsule = {
		"version": CAPSULE_VERSION,
		"created_utc": datetime.now(timezone.utc).isoformat(),
		"source_name": source_name,
		"source_type": source_type,
		"sha256": sha256_bytes(payload),
		"payload_b64": base64.b64encode(payload).decode("ascii"),
	}
	token = Fernet(key).encrypt(json.dumps(capsule, sort_keys=True).encode("utf-8"))
	return token, key.decode("ascii")


def open_capsule(token: bytes, key: str) -> dict[str, object]:
	"""Decrypt and validate the capsule envelope without trusting its metadata."""
	decrypted = Fernet(key.encode("ascii")).decrypt(token)
	capsule = json.loads(decrypted.decode("utf-8"))
	payload = base64.b64decode(capsule["payload_b64"])
	expected_hash = capsule["sha256"]
	actual_hash = sha256_bytes(payload)
	capsule["payload"] = payload
	capsule["actual_sha256"] = actual_hash
	capsule["integrity_ok"] = hmac.compare_digest(actual_hash, expected_hash)
	return capsule


def write_capsule(path: Path, token: bytes, key: str) -> None:
	path.write_text(json.dumps({"key": key, "token": token.decode("ascii")}, indent=2), encoding="utf-8")


class CapsuleApp(tk.Tk):
	def __init__(self, role: str):
		super().__init__()
		self.role = role
		self.title("Integrity Capsule")
		self.geometry("820x650")
		self.minsize(700, 540)
		self.configure(background="#eef3f4")
		self.current_token: bytes | None = None
		self.current_key = ""
		self.source_name = "Message"
		self.source_type = "text"

		style = ttk.Style(self)
		style.theme_use("clam")
		style.configure("App.TFrame", background="#eef3f4")
		style.configure("Header.TFrame", background="#16324f")
		style.configure("Title.TLabel", background="#16324f", foreground="#f7fbfc", font=("Segoe UI", 20, "bold"))
		style.configure("Header.TLabel", background="#16324f", foreground="#b9d9d7", font=("Segoe UI", 10))
		style.configure("Section.TLabel", background="#ffffff", foreground="#16324f", font=("Segoe UI", 10, "bold"))
		style.configure("Subtitle.TLabel", background="#eef3f4", foreground="#52606d")
		style.configure("Status.TLabel", background="#dcefee", foreground="#164e63", padding=10, wraplength=740)
		style.configure("TNotebook", background="#eef3f4", borderwidth=0)
		style.configure("TNotebook.Tab", background="#d7e2e4", foreground="#29434a", padding=(16, 8))
		style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#0f5c62")])
		style.configure("TButton", font=("Segoe UI", 10), padding=(12, 7))
		style.configure("Accent.TButton", background="#0f766e", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
		style.map("Accent.TButton", background=[("active", "#115e59"), ("pressed", "#134e4a")])
		style.configure("Panel.TFrame", background="#ffffff", relief="solid", borderwidth=1)

		header = ttk.Frame(self, style="Header.TFrame", padding=(28, 22, 28, 18))
		header.pack(fill="x")
		ttk.Label(header, text="Integrity Capsule", style="Title.TLabel").pack(anchor="w")
		ttk.Label(
			header,
			text=f"SECURE HANDOFF  /  SIGNED IN AS {role.upper()}",
			style="Header.TLabel",
		).pack(anchor="w", pady=(4, 0))

		tabs = ttk.Notebook(self)
		tabs.pack(fill="both", expand=True, padx=24, pady=(8, 24))
		self.build_create_tab(tabs)
		self.build_open_tab(tabs)

	def add_text_box(self, parent: ttk.Frame, label: str, height: int = 8) -> tk.Text:
		ttk.Label(parent, text=label, style="Section.TLabel").pack(anchor="w", pady=(4, 6))
		field = tk.Text(
			parent,
			height=height,
			wrap="word",
			relief="flat",
			borderwidth=0,
			background="#f7faf9",
			foreground="#25343b",
			insertbackground="#0f766e",
			padx=10,
			pady=10,
			font=("Segoe UI", 10),
		)
		field.pack(fill="both", expand=True)
		return field

	def build_create_tab(self, tabs: ttk.Notebook) -> None:
		tab = ttk.Frame(tabs, style="App.TFrame", padding=20)
		tabs.add(tab, text="Create Capsule")
		ttk.Label(tab, text="Protect a message or file with encryption plus a visible integrity fingerprint.", style="Subtitle.TLabel").pack(anchor="w", pady=(0, 4))
		input_panel = ttk.Frame(tab, style="Panel.TFrame", padding=14)
		input_panel.pack(fill="both", expand=True, pady=(8, 0))
		self.input_box = self.add_text_box(input_panel, "MESSAGE OR FILE CONTENT", height=9)
		controls = ttk.Frame(tab)
		controls.pack(fill="x", pady=12)
		ttk.Button(controls, text="Choose file instead", command=self.choose_file).pack(side="left")
		ttk.Button(controls, text="Create encrypted capsule", style="Accent.TButton", command=self.create).pack(side="left", padx=8)
		self.create_status = ttk.Label(tab, text="No capsule created yet.", style="Status.TLabel")
		self.create_status.pack(anchor="w", pady=(4, 0))

	def build_open_tab(self, tabs: ttk.Notebook) -> None:
		tab = ttk.Frame(tabs, style="App.TFrame", padding=20)
		tabs.add(tab, text="Open and Verify")
		ttk.Label(tab, text="Open a saved capsule, recover the payload, and compare its hashes.", style="Subtitle.TLabel").pack(anchor="w", pady=(0, 4))
		buttons = ttk.Frame(tab)
		buttons.pack(fill="x", pady=12)
		ttk.Button(buttons, text="Open capsule file", style="Accent.TButton", command=self.open_saved).pack(side="left")
		ttk.Button(buttons, text="Test tamper detection", command=self.test_tamper).pack(side="left", padx=8)
		output_panel = ttk.Frame(tab, style="Panel.TFrame", padding=14)
		output_panel.pack(fill="both", expand=True)
		self.output_box = self.add_text_box(output_panel, "DECRYPTED OUTPUT", height=9)
		self.open_status = ttk.Label(tab, text="No capsule opened yet.", style="Status.TLabel")
		self.open_status.pack(anchor="w", pady=(8, 0))

	def choose_file(self) -> None:
		file_path = filedialog.askopenfilename(title="Choose a file to protect")
		if not file_path:
			return
		try:
			data = Path(file_path).read_bytes()
		except OSError as error:
			messagebox.showerror("Could not read file", str(error))
			return
		self.input_box.insert("1.0", data.decode("utf-8", errors="replace"))
		self.source_name = Path(file_path).name
		self.source_type = "file"
		self.create_status.config(text=f"Loaded {self.source_name}; create the capsule to protect it.")
	
	def create(self) -> None:
		text = self.input_box.get("1.0", "end-1c")
		if not text:
			messagebox.showwarning("Nothing to protect", "Enter a message or choose a file first.")
			return
		payload = text.encode("utf-8")
		self.current_token, self.current_key = make_capsule(payload, self.source_name, self.source_type)
		default_name = "secure_capsule.json"
		path = filedialog.asksaveasfilename(defaultextension=".json", initialfile=default_name, filetypes=[("Capsule files", "*.json")])
		if path:
			try:
				write_capsule(Path(path), self.current_token, self.current_key)
			except OSError as error:
				messagebox.showerror("Could not save capsule", str(error))
				return
		self.create_status.config(text=f"Encrypted {self.source_name}. SHA-256: {sha256_bytes(payload)}\nKey is kept in the capsule file for this classroom demonstration.")

	def open_saved(self) -> None:
		path = filedialog.askopenfilename(title="Open a capsule", filetypes=[("Capsule files", "*.json")])
		if not path:
			return
		try:
			stored = json.loads(Path(path).read_text(encoding="utf-8"))
			self.current_token = stored["token"].encode("ascii")
			self.current_key = stored["key"]
			capsule = open_capsule(self.current_token, self.current_key)
		except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError, InvalidToken) as error:
			messagebox.showerror("Could not open capsule", f"The capsule could not be decrypted or parsed.\n\n{error}")
			return
		self.show_capsule(capsule)

	def show_capsule(self, capsule: dict[str, object]) -> None:
		payload = capsule["payload"]
		self.output_box.delete("1.0", "end")
		self.output_box.insert("1.0", payload.decode("utf-8", errors="replace"))
		status = "PASS: decrypted payload matches its recorded SHA-256." if capsule["integrity_ok"] else "FAIL: decrypted payload does not match its recorded SHA-256."
		self.open_status.config(text=f"{status}\nExpected: {capsule['sha256']}\nActual:   {capsule['actual_sha256']}")

	def test_tamper(self) -> None:
		if self.current_token is None:
			messagebox.showinfo("Create a capsule first", "Open or create a capsule before running the tamper test.")
			return
		altered = bytearray(self.current_token)
		altered[-1] = altered[-1] ^ 1
		try:
			open_capsule(bytes(altered), self.current_key)
		except InvalidToken:
			self.open_status.config(text="PASS: tampering was rejected by Fernet authentication before plaintext was released.")
		else:
			self.open_status.config(text="The altered capsule still decrypted; the integrity comparison should be inspected.")


def launch_gui(role: str) -> None:
	CapsuleApp(role).mainloop()


def main() -> None:
	create_demo_users()
	print("Integrity Capsule")
	print("Demo credentials: admin / Admin123! or student / Student123!")
	if "--console" in sys.argv:
		username = input("Username: ").strip()
		password = getpass.getpass("Password: ")
	else:
		login = tk.Tk()
		login.title("Integrity Capsule Login")
		login.geometry("360x250")
		login.resizable(False, False)
		login.configure(background="#eef3f4")
		header = tk.Frame(login, background="#16324f", height=72)
		header.pack(fill="x")
		tk.Label(header, text="INTEGRITY CAPSULE", foreground="#f7fbfc", background="#16324f", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=24, pady=(15, 2))
		tk.Label(header, text="SECURE HANDOFF LAB", foreground="#b9d9d7", background="#16324f", font=("Segoe UI", 9)).pack(anchor="w", padx=24)
		frame = tk.Frame(login, background="#eef3f4", padx=28, pady=18)
		frame.pack(fill="both", expand=True)
		tk.Label(frame, text="Integrity Capsule", font=("Segoe UI", 16, "bold")).pack(pady=(0, 18))
		tk.Label(frame, text="Username", foreground="#16324f", background="#eef3f4", font=("Segoe UI", 10, "bold")).pack(anchor="w")
		username_entry = ttk.Entry(frame)
		username_entry.pack(fill="x", pady=(3, 10))
		tk.Label(frame, text="Password", foreground="#16324f", background="#eef3f4", font=("Segoe UI", 10, "bold")).pack(anchor="w")
		password_entry = ttk.Entry(frame, show="*")
		password_entry.pack(fill="x", pady=(3, 16))
		login_data: dict[str, str] = {}

		def submit_login() -> None:
			login_data["username"] = username_entry.get().strip()
			login_data["password"] = password_entry.get()
			login.destroy()

		ttk.Button(frame, text="Sign in", command=submit_login).pack(fill="x")
		login.bind("<Return>", lambda _event: submit_login())
		username_entry.focus_set()
		login.mainloop()
		username = login_data.get("username", "")
		password = login_data.get("password", "")
	role = authenticate(username, password)
	if role is None:
		print("Login failed.")
		return
	launch_gui(role) if "--console" not in sys.argv else print("Console mode is available for credential testing; run the GUI for the capsule workflow.")


if __name__ == "__main__":
	main()