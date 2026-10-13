import tempfile
import unittest
from pathlib import Path

from secret_scanner import scan_path


class SecretScannerTests(unittest.TestCase):
    def test_detects_secret_patterns_and_line_numbers(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "example.txt"
            filename.write_text(
                "nothing here\n"
                "password = 'fake-password-123'\n"
                f"access key: {'AKIA' + 'A' * 16}\n",
                encoding="utf-8",
            )

            findings = scan_path(filename)

        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0].line_number, 2)
        self.assertEqual(findings[0].pattern_name, "Password or secret assignment")
        self.assertEqual(findings[1].line_number, 3)
        self.assertEqual(findings[1].pattern_name, "AWS access key")

    def test_scans_files_in_subdirectories(self):
        with tempfile.TemporaryDirectory() as folder:
            nested = Path(folder) / "nested"
            nested.mkdir()
            filename = nested / "settings.txt"
            fake_token = "ghp_" + "a" * 25
            filename.write_text(
                f"token=generic-secret-value\n{fake_token}\n", encoding="utf-8"
            )

            findings = scan_path(folder)

        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0].filename, filename)
        self.assertEqual(findings[0].pattern_name, "Password or secret assignment")
        self.assertEqual(findings[1].pattern_name, "GitHub token")

    def test_detects_other_included_pattern_families(self):
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "keys.txt"
            filename.write_text(
                f"{'AIza' + 'A' * 35}\n"
                f"{'xoxb-' + 'a' * 15}\n"
                f"{'sk_live_' + 'a' * 24}\n"
                "-----BEGIN PRIVATE KEY-----\n",
                encoding="utf-8",
            )

            findings = scan_path(filename)

        self.assertEqual(
            [finding.pattern_name for finding in findings],
            [
                "Google API key",
                "Slack token",
                "Stripe secret key",
                "Private key header",
            ],
        )

    def test_reports_missing_path(self):
        with tempfile.TemporaryDirectory() as folder:
            missing = Path(folder) / "missing.txt"

            with self.assertRaises(FileNotFoundError):
                scan_path(missing)


if __name__ == "__main__":
    unittest.main()
