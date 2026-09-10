""" 
Victor Delgado
09/08/2026
Mod. 3 Secure Hashing
SDEV-245
"""

"""Module 3 security demonstration.

This console application demonstrates authentication, role-based access
control, a Caesar cipher, SHA-256 integrity checks, and RSA signatures.
It is intentionally educational and is not a production authentication
system. It uses tkinter for a GUI interface, but can also run in console mode with the
 --console command line argument. The demo creates two users with hard-coded
credentials: admin / Admin123! and student / Student123!. 
The admin user can access all features, while the student user has limited access. 
The application uses PBKDF2 for password hashing, SHA-256 for hashing text and files, 
and RSA for digital signatures.
"""

from __future__ import annotations

import base64
import getpass
import hashlib
import hmac
import secrets
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding, rsa


PBKDF2_ROUNDS = 120_000
USERS = {
	"admin": {"role": "admin", "password_hash": ""},
	"student": {"role": "student", "password_hash": ""},
}


def password_digest(password: str, salt: bytes) -> str:
	"""Return a salted PBKDF2 password digest suitable for this demo."""
	digest = hashlib.pbkdf2_hmac(
		"sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS
	)
	return f"{salt.hex()}${digest.hex()}"


def create_demo_users() -> None:
	"""Create fresh salted demo credentials at startup."""
	for username, password in (("admin", "Admin123!"), ("student", "Student123!")):
		salt = secrets.token_bytes(16)
		USERS[username]["password_hash"] = password_digest(password, salt)


def authenticate(username: str, password: str) -> str | None:
	"""Return a user's role when credentials are valid."""
	account = USERS.get(username)
	if account is None:
		return None
	salt_hex, expected_hex = account["password_hash"].split("$")
	actual_hex = password_digest(password, bytes.fromhex(salt_hex)).split("$")[1]
	if hmac.compare_digest(actual_hex, expected_hex):
		return account["role"]
	return None


def require_role(role: str, allowed_roles: set[str]) -> bool:
	"""Enforce authorization at the operation boundary."""
	if role not in allowed_roles:
		print(f"Access denied: the {role} role cannot use this feature.")
		return False
	return True


def caesar_cipher(text: str, shift: int) -> str:
	"""Encrypt or decrypt text while preserving case and punctuation."""
	result = []
	for character in text:
		if character.isascii() and character.isalpha():
			base = ord("A") if character.isupper() else ord("a")
			result.append(chr((ord(character) - base + shift) % 26 + base))
		else:
			result.append(character)
	return "".join(result)


def sha256_text(text: str) -> str:
	"""Return the SHA-256 digest of UTF-8 encoded text."""
	return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(file_path: str) -> str:
	"""Hash a file in chunks so large files do not fill memory."""
	digest = hashlib.sha256()
	with Path(file_path).open("rb") as input_file:
		for chunk in iter(lambda: input_file.read(8192), b""):
			digest.update(chunk)
	return digest.hexdigest()


def create_signature_keys() -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
	private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
	return private_key, private_key.public_key()


def sign_message(message: str, private_key: rsa.RSAPrivateKey) -> str:
	"""Sign a message with the private key and return portable base64 text."""
	signature = private_key.sign(
		message.encode("utf-8"),
		padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
		hashes.SHA256(),
	)
	return base64.b64encode(signature).decode("ascii")


def verify_signature(message: str, signature: str, public_key: rsa.RSAPublicKey) -> bool:
	try:
		public_key.verify(
			base64.b64decode(signature),
			message.encode("utf-8"),
			padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
			hashes.SHA256(),
		)
		return True
	except (InvalidSignature, ValueError, TypeError):
		return False


def show_menu(role: str, private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey) -> None:
	while True:
		print("\n1. Caesar encrypt/decrypt")
		print("2. SHA-256 text hash")
		print("3. SHA-256 file hash")
		print("4. Sign and verify a message (admin only)")
		print("5. Quit")
		choice = input("Choose an option: ").strip()

		if choice == "1":
			message = input("Message: ")
			shift = int(input("Shift (use a negative value to decrypt): "))
			print(f"Result: {caesar_cipher(message, shift)}")
		elif choice == "2":
			print(f"SHA-256: {sha256_text(input('Text: '))}")
		elif choice == "3":
			try:
				print(f"SHA-256: {sha256_file(input('File path: ').strip())}")
			except (OSError, ValueError) as error:
				print(f"Could not hash file: {error}")
		elif choice == "4":
			if require_role(role, {"admin"}):
				message = input("Message to sign: ")
				signature = sign_message(message, private_key)
				print(f"Signature: {signature}")
				print(f"Verification: {verify_signature(message, signature, public_key)}")
				print(f"Tampered verification: {verify_signature(message + ' changed', signature, public_key)}")
		elif choice == "5":
			print("Goodbye.")
			return
		else:
			print("Please choose a number from 1 to 5.")


class SecurityDemoApp(tk.Tk):
	"""Tkinter interface for the Module 3 demonstrations."""

	def __init__(self, role: str, private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey):
		super().__init__()
		self.role = role
		self.private_key = private_key
		self.public_key = public_key
		self.title("Module 3 Security Demo")
		self.geometry("760x560")
		self.minsize(650, 480)

		style = ttk.Style(self)
		if "vista" in style.theme_names():
			style.theme_use("vista")
		style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
		style.configure("Subtitle.TLabel", foreground="#52606d")
		style.configure("Result.TLabel", foreground="#075985", wraplength=680)

		header = ttk.Frame(self, padding=(24, 20, 24, 8))
		header.pack(fill="x")
		ttk.Label(header, text="Module 3 Security Demo", style="Title.TLabel").pack(anchor="w")
		ttk.Label(
			header,
			text=f"Signed in as {role}  |  Role-based access is active",
			style="Subtitle.TLabel",
		).pack(anchor="w", pady=(4, 0))

		self.notebook = ttk.Notebook(self)
		self.notebook.pack(fill="both", expand=True, padx=24, pady=(8, 24))
		self.build_cipher_tab()
		self.build_hash_tab()
		self.build_signature_tab()
		if role != "admin":
			self.notebook.tab(2, state="disabled")

	def add_labeled_text(self, parent: ttk.Frame, label: str, height: int = 5) -> tk.Text:
		ttk.Label(parent, text=label).pack(anchor="w", pady=(12, 4))
		field = tk.Text(parent, height=height, wrap="word", relief="solid", borderwidth=1)
		field.pack(fill="x")
		return field

	def build_cipher_tab(self) -> None:
		tab = ttk.Frame(self.notebook, padding=20)
		self.notebook.add(tab, text="Caesar Cipher")
		ttk.Label(tab, text="Shift letters to encrypt or decrypt text.", style="Subtitle.TLabel").pack(anchor="w")
		self.cipher_input = self.add_labeled_text(tab, "Input message")
		controls = ttk.Frame(tab)
		controls.pack(fill="x", pady=12)
		ttk.Label(controls, text="Shift:").pack(side="left")
		self.shift = ttk.Spinbox(controls, from_=-100, to=100, width=8)
		self.shift.set(3)
		self.shift.pack(side="left", padx=(8, 16))
		ttk.Button(controls, text="Encrypt", command=lambda: self.run_cipher(1)).pack(side="left", padx=4)
		ttk.Button(controls, text="Decrypt", command=lambda: self.run_cipher(-1)).pack(side="left", padx=4)
		self.cipher_result = ttk.Label(tab, text="", style="Result.TLabel")
		self.cipher_result.pack(anchor="w", pady=12)

	def run_cipher(self, direction: int) -> None:
		try:
			shift = int(self.shift.get()) * direction
			result = caesar_cipher(self.cipher_input.get("1.0", "end-1c"), shift)
			self.cipher_result.config(text=f"Result: {result}")
		except ValueError:
			messagebox.showerror("Invalid shift", "Enter a whole number for the shift.")

	def build_hash_tab(self) -> None:
		tab = ttk.Frame(self.notebook, padding=20)
		self.notebook.add(tab, text="SHA-256 Integrity")
		ttk.Label(tab, text="Generate a SHA-256 digest for text or a file.", style="Subtitle.TLabel").pack(anchor="w")
		self.hash_input = self.add_labeled_text(tab, "Text to hash", height=4)
		ttk.Button(tab, text="Hash text", command=self.hash_text).pack(anchor="w", pady=(10, 6))
		ttk.Button(tab, text="Choose file and hash", command=self.hash_file).pack(anchor="w")
		self.hash_result = ttk.Label(tab, text="", style="Result.TLabel")
		self.hash_result.pack(anchor="w", pady=16)

	def hash_text(self) -> None:
		digest = sha256_text(self.hash_input.get("1.0", "end-1c"))
		self.hash_result.config(text=f"SHA-256: {digest}")

	def hash_file(self) -> None:
		file_path = filedialog.askopenfilename(title="Choose a file to hash")
		if not file_path:
			return
		try:
			self.hash_result.config(text=f"SHA-256 ({Path(file_path).name}): {sha256_file(file_path)}")
		except OSError as error:
			messagebox.showerror("Could not hash file", str(error))

	def build_signature_tab(self) -> None:
		tab = ttk.Frame(self.notebook, padding=20)
		self.notebook.add(tab, text="Digital Signature")
		ttk.Label(tab, text="Admin-only: sign a message and verify its integrity.", style="Subtitle.TLabel").pack(anchor="w")
		self.signature_input = self.add_labeled_text(tab, "Message to sign", height=4)
		ttk.Button(tab, text="Sign and verify", command=self.sign_and_verify).pack(anchor="w", pady=12)
		self.signature_result = ttk.Label(tab, text="", style="Result.TLabel")
		self.signature_result.pack(anchor="w", pady=8)

	def sign_and_verify(self) -> None:
		message = self.signature_input.get("1.0", "end-1c")
		signature = sign_message(message, self.private_key)
		valid = verify_signature(message, signature, self.public_key)
		tampered = verify_signature(message + " changed", signature, self.public_key)
		self.signature_result.config(
			text=f"Valid signature: {valid}\nTampered message accepted: {tampered}\n\nSignature:\n{signature}"
		)


def launch_gui(role: str, private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey) -> None:
	app = SecurityDemoApp(role, private_key, public_key)
	app.mainloop()


def main() -> None:
	create_demo_users()
	print("Module 3 Security Demo")
	print("Demo credentials: admin / Admin123! or student / Student123!")
	if "--console" in sys.argv:
		username = input("Username: ").strip()
		password = getpass.getpass("Password: ")
	else:
		login = tk.Tk()
		login.title("Module 3 Login")
		login.geometry("360x250")
		login.resizable(False, False)
		login.columnconfigure(0, weight=1)
		frame = ttk.Frame(login, padding=28)
		frame.pack(fill="both", expand=True)
		ttk.Label(frame, text="Module 3 Security Demo", font=("Segoe UI", 16, "bold")).pack(pady=(0, 18))
		ttk.Label(frame, text="Username").pack(anchor="w")
		username_entry = ttk.Entry(frame)
		username_entry.pack(fill="x", pady=(3, 10))
		ttk.Label(frame, text="Password").pack(anchor="w")
		password_entry = ttk.Entry(frame, show="*")
		password_entry.pack(fill="x", pady=(3, 16))
		login_data = {}

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

	print(f"Login successful. Role: {role}")
	private_key, public_key = create_signature_keys()
	if "--console" in sys.argv:
		show_menu(role, private_key, public_key)
	else:
		launch_gui(role, private_key, public_key)


if __name__ == "__main__":
	main()
