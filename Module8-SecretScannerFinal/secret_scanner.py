"""Scan files for common patterns that may indicate hardcoded secrets."""

import argparse
import logging
import re
from dataclasses import dataclass
from pathlib import Path


# Each entry has a name for the report and a regex for one kind of secret.
# These check the shape of a value; they cannot prove that a key is still active.
PATTERNS = {
    # Common provider-specific prefixes make these token types easier to spot.
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
    "Stripe secret key": re.compile(r"\bsk_live_[0-9A-Za-z]{20,}\b"),
    # This catches assignments such as password="..." or api_key: "...".
    # The pattern is split across strings to keep the expression readable.
    "Password or secret assignment": re.compile(
        r"""(?i)["']?\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|"""
        r"""client[_-]?secret|password|passwd|secret|token)["']?\s*[:=]\s*"""
        r"""["']?[^\s"'#,;]{4,}"""
    ),
    # Private-key files often start with one of these PEM header lines.
    "Private key header": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"
    ),
}


@dataclass
class Finding:
    # Keep the details together so both the CLI and GUI can show the same result.
    filename: Path
    line_number: int
    pattern_name: str
    matched_text: str


def scan_file(filename):
    """Return potential secrets found in one readable text file."""
    findings = []

    try:
        # Replace decoding errors so one unusual character does not stop the scan.
        with filename.open("r", encoding="utf-8", errors="replace") as source:
            # Counting starts at 1 so the reported line matches most text editors.
            for line_number, line in enumerate(source, start=1):
                # Check every pattern on each line and save every match.
                for pattern_name, pattern in PATTERNS.items():
                    for match in pattern.finditer(line):
                        findings.append(
                            Finding(
                                filename=filename,
                                line_number=line_number,
                                pattern_name=pattern_name,
                                matched_text=match.group(0),
                            )
                        )
    except OSError as error:
        # A file may be unreadable, so log it and continue with other files.
        logging.warning("Could not read %s: %s", filename, error)

    return findings


def scan_path(path):
    """Scan a single file or all files below a directory."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    if not path.is_file() and not path.is_dir():
        raise ValueError(f"Path is not a file or directory: {path}")

    # A directory scan includes files inside its subfolders too.
    files = [path] if path.is_file() else sorted(
        item for item in path.rglob("*") if item.is_file()
    )

    # Collect each file's results into one report.
    findings = []
    for filename in files:
        findings.extend(scan_file(filename))
    return findings


def print_report(findings):
    """Print scan results in a readable format."""
    if not findings:
        print("No possible secrets found.")
        return

    # Show where the match came from along with the text that matched.
    print(f"Found {len(findings)} possible secret(s):")
    for finding in findings:
        print(
            f"{finding.filename}:{finding.line_number} "
            f"[{finding.pattern_name}] {finding.matched_text}"
        )


def launch_gui():
    """Open the Tkinter interface."""
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.title("Secret Scanner")
    root.geometry("850x450")

    selected_path = tk.StringVar(value="Choose a file or folder to scan")
    status = tk.StringVar(value="Ready")

    # The table keeps the same filename, line, and match details as the CLI.
    ttk.Label(root, textvariable=selected_path, wraplength=800).pack(
        padx=10, pady=(10, 5), anchor="w"
    )

    columns = ("filename", "line", "pattern", "match")
    results = ttk.Treeview(root, columns=columns, show="headings")
    results.heading("filename", text="Filename")
    results.heading("line", text="Line")
    results.heading("pattern", text="Pattern")
    results.heading("match", text="Matched string")
    results.column("filename", width=260)
    results.column("line", width=55, anchor="center")
    results.column("pattern", width=190)
    results.column("match", width=320)
    results.pack(fill="both", expand=True, padx=10, pady=5)

    def choose_file():
        # The file picker returns an empty value if the user cancels.
        filename = filedialog.askopenfilename(title="Choose a file to scan")
        if filename:
            selected_path.set(filename)

    def choose_folder():
        # The folder picker lets the scanner search the selected folder recursively.
        folder = filedialog.askdirectory(title="Choose a folder to scan")
        if folder:
            selected_path.set(folder)

    def scan_selected_path():
        path = selected_path.get()
        if path == "Choose a file or folder to scan":
            messagebox.showinfo("Choose a path", "Choose a file or folder first.")
            return

        # Show path problems in the window instead of closing the GUI.
        try:
            findings = scan_path(path)
        except (OSError, ValueError) as error:
            messagebox.showerror("Scan error", str(error))
            return

        # Clear old results before displaying this scan's findings.
        results.delete(*results.get_children())
        for finding in findings:
            results.insert(
                "",
                "end",
                values=(
                    str(finding.filename),
                    finding.line_number,
                    finding.pattern_name,
                    finding.matched_text,
                ),
            )
        status.set(f"Scan complete: {len(findings)} possible secret(s) found.")

    buttons = ttk.Frame(root)
    buttons.pack(fill="x", padx=10, pady=5)
    ttk.Button(buttons, text="Choose file", command=choose_file).pack(
        side="left", padx=(0, 5)
    )
    ttk.Button(buttons, text="Choose folder", command=choose_folder).pack(
        side="left", padx=5
    )
    ttk.Button(buttons, text="Scan", command=scan_selected_path).pack(
        side="left", padx=5
    )
    ttk.Label(root, textvariable=status).pack(padx=10, pady=(0, 10), anchor="w")

    root.mainloop()


def main():
    # argparse handles --help and reads either an input path or the GUI option.
    parser = argparse.ArgumentParser(
        description="Find common hardcoded secret patterns in files and folders."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="File or directory to scan (not needed when using --gui)",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Open the graphical interface",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # The GUI can be started explicitly with --gui or by running with no path.
    if args.gui:
        if args.path:
            parser.error("Do not provide a path when using --gui.")
        launch_gui()
        return 0
    if not args.path:
        launch_gui()
        return 0

    # A bad path is an error, while a successful scan prints its findings.
    try:
        findings = scan_path(args.path)
    except (OSError, ValueError) as error:
        logging.error("%s", error)
        return 2

    print_report(findings)
    return 1 if findings else 0


if __name__ == "__main__":
    # Use the returned status as the program's command-line exit code.
    raise SystemExit(main())
