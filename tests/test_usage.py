"""Unit tests for usage.parse_winget (the table printed by `winget upgrade`).

Run from the project folder:  python -m unittest discover -s tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from usage import parse_winget  # noqa: E402


def table(*rows, head="Name Id Version Available Source", widths=(30, 28, 14, 14)):
    """Build a winget-like table: header padded to `widths`, a dash rule, then the rows padded the same way."""
    def line(cells):
        padded = [c.ljust(w) for c, w in zip(cells, widths)] + list(cells[len(widths):])
        return "".join(padded).rstrip()
    lines = [line(head.split(" ") if isinstance(head, str) else head), "-" * (sum(widths) + 6)]
    return "\n".join(lines + [line(r) for r in rows])


class ParseWingetTest(unittest.TestCase):

    def test_typical_output(self):
        text = table(("Git", "Git.Git", "2.45.1", "2.46.0", "winget"),
                     ("Microsoft Edge", "Microsoft.Edge", "130.0.2849.80", "131.0.2903.51", "winget"))
        text += "\n2 upgrades available.\n"
        self.assertEqual(parse_winget(text), [
            {"nome": "Git", "id": "Git.Git", "atual": "2.45.1", "nova": "2.46.0", "origem": "winget"},
            {"nome": "Microsoft Edge", "id": "Microsoft.Edge", "atual": "130.0.2849.80", "nova": "131.0.2903.51",
             "origem": "winget"},
        ])

    def test_different_column_widths(self):
        rows = [("7-Zip 24.07 (x64)", "7zip.7zip", "24.07", "24.08", "winget")]
        narrow = parse_winget(table(*rows, widths=(19, 11, 9, 11)))
        wide = parse_winget(table(*rows, widths=(50, 40, 20, 20)))
        expected = [{"nome": "7-Zip 24.07 (x64)", "id": "7zip.7zip", "atual": "24.07", "nova": "24.08", "origem": "winget"}]
        self.assertEqual(narrow, expected)
        self.assertEqual(wide, expected)

    def test_localized_header(self):
        """The header is translated by winget; only the column positions matter."""
        text = table(("Notepad++", "Notepad++.Notepad++", "8.6.9", "8.7.1", "winget"),
                     head=["Nome", "ID", "Versão", "Disponível", "Origem"])
        self.assertEqual(parse_winget(text)[0]["id"], "Notepad++.Notepad++")

    def test_progress_spinner_and_crlf(self):
        """winget draws a spinner with carriage returns before the table and ends lines with CRLF."""
        body = table(("Git", "Git.Git", "2.45.1", "2.46.0", "winget"))
        text = "   - \r   \\ \r   | \r" + body.replace("\n", "\r\n") + "\r\n1 upgrades available.\r\n"
        self.assertEqual([u["id"] for u in parse_winget(text)], ["Git.Git"])

    def test_without_source_column(self):
        text = table(("Git", "Git.Git", "2.45.1", "2.46.0"), head="Name Id Version Available")
        self.assertEqual(parse_winget(text), [
            {"nome": "Git", "id": "Git.Git", "atual": "2.45.1", "nova": "2.46.0", "origem": ""}])

    def test_msstore_source_is_kept(self):
        """Filtering Store apps is match_updates' job; the parser keeps the source."""
        text = table(("Spotify", "9NCBCSZSJRSB", "1.2.3", "1.2.4", "msstore"))
        self.assertEqual(parse_winget(text)[0]["origem"], "msstore")

    def test_only_first_table(self):
        """A second table ("require explicit targeting") after a blank line is ignored."""
        first = table(("Git", "Git.Git", "2.45.1", "2.46.0", "winget"))
        second = table(("Discord", "Discord.Discord", "1.0.9163", "1.0.9164", "winget"))
        text = first + "\n1 upgrades available.\n\nThe following packages require explicit targeting:\n" + second
        self.assertEqual([u["id"] for u in parse_winget(text)], ["Git.Git"])

    def test_rows_stop_at_blank_line(self):
        text = table(("Git", "Git.Git", "2.45.1", "2.46.0", "winget")) + "\n\n" + "Python 3 Python.Python.3 1 2 winget"
        self.assertEqual(len(parse_winget(text)), 1)

    def test_skips_rows_without_id_or_new_version(self):
        text = table(("Git", "Git.Git", "2.45.1", "2.46.0", "winget"),
                     ("Broken row", "", "1.0", "", ""),
                     ("Has space", "Not An Id", "1.0", "2.0", "winget"))
        self.assertEqual([u["id"] for u in parse_winget(text)], ["Git.Git"])

    def test_empty_list(self):
        self.assertEqual(parse_winget("No installed package found matching input criteria.\n"), [])

    def test_empty_text(self):
        self.assertEqual(parse_winget(""), [])

    def test_no_header(self):
        """A dash rule without a usable header (fewer than 4 columns) gives no result."""
        self.assertEqual(parse_winget("Something\n--------------------\nGit Git.Git 2.45.1 2.46.0\n"), [])
        self.assertEqual(parse_winget("Git Git.Git 2.45.1 2.46.0 winget\n"), [])


if __name__ == "__main__":
    unittest.main()
