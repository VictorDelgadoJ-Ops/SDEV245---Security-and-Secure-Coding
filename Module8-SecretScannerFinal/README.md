# Module 8: Secret Scanner

## Project overview

This project is a small Python tool that looks through a file or folder for
text that could be a hardcoded password, API key, token, or private key. I made
it for practicing secure coding and regular expressions. It has a command-line
interface (CLI) and a basic graphical interface (GUI), so the scanner can be
used from a terminal or by choosing a file or folder in a window.

The scanner uses only Python's standard library, so there are no extra
packages to install. The GUI uses Tkinter, which is included with most Python
installations.

## What the scanner checks

The program checks each line against seven regular expressions:

| Pattern | What it looks for |
| --- | --- |
| AWS access key | `AKIA` followed by 16 uppercase letters or numbers |
| GitHub token | Common GitHub token prefixes, such as `ghp_` or `gho_` |
| Google API key | `AIza` followed by 35 characters from the expected set |
| Slack token | Common Slack token prefixes starting with `xox` |
| Stripe secret key | A key starting with `sk_live_` |
| Password or secret assignment | Assignments using names like `password`, `api_key`, `token`, or `secret` |
| Private key header | A PEM header such as `-----BEGIN PRIVATE KEY-----` |

The provider-specific examples were informed by
[odomojuli/regextokens](https://github.com/odomojuli/regextokens). These
regular expressions only check whether text has a familiar shape. They do not
check whether a credential is real, active, or usable.

## Files in this project

- `secret_scanner.py` contains the scanning functions, CLI, and Tkinter GUI.
- `secret_scanner_gui.py` opens the GUI directly.
- `test_secret_scanner.py` contains unit tests for the scanning behavior.
- `scanner-demo.txt` has fake sample values for testing a single file.
- `demo-scan/` has fake sample values in multiple files for testing folder
  scanning, including a nested folder.

The demo values are made up and should not be used as actual credentials.

## Requirements and setup

Use Python 3. The project does not need third-party packages. Open a terminal
and change into this project folder:

```text
cd Module8-SecretScannerFinal
```

If Python is installed, you can run the commands below with `python`. On some
Windows computers, the Python launcher is `py`, so `py` can be used instead.

## Using the CLI

To scan one file:

```text
python secret_scanner.py scanner-demo.txt
```

To scan a folder and the files in its subfolders:

```text
python secret_scanner.py demo-scan
```

The CLI prints the filename, line number, pattern name, and matched text for
each possible secret. For example, the output will look similar to this:

```text
Found 3 possible secret(s):
scanner-demo.txt:2 [Password or secret assignment] password = "fake-password-123
```

The program also uses logging to report problems such as files it cannot read
or an invalid input path. Its exit codes are:

- `0` — scan completed with no matches
- `1` — scan completed and possible secrets were found
- `2` — the path could not be scanned

## Using the GUI

To open the GUI directly:

```text
python secret_scanner_gui.py
```

You can also run `python secret_scanner.py --gui` or run
`python secret_scanner.py` without a path.

In the window, choose **Choose file** or **Choose folder**, select
`scanner-demo.txt` or the `demo-scan` folder, and click **Scan**. The results
table shows the filename, line, type of pattern, and matched string. Choosing a
folder also checks its subfolders.

## Running the tests

The tests use Python's built-in `unittest` module. From this folder, run:

```text
python -m unittest discover -v
```

The tests check that the scanner detects sample values, reports line numbers,
finds files in subfolders, and handles a path that does not exist.

## Limits and safe use

This is a basic learning project, not a full security scanner. It can report
false positives, and it can miss credentials that do not match its patterns.
For example, it does not know whether a matched key is valid, and the general
assignment pattern cannot identify every possible name or code style.

The scanner prints matched text, which could expose a real credential in the
terminal or GUI. Only scan files you are allowed to inspect, and use fake
values for demonstrations.
