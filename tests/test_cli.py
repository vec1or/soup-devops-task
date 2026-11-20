"""Source-level checks; these do not prove the built distribution works."""

import io
import platform
import unittest
from contextlib import redirect_stdout
from importlib.metadata import version

from soupcheck.cli import main


class CliTests(unittest.TestCase):
    def test_report_reads_message_and_describes_runtime(self):
        output = io.StringIO()
        with redirect_stdout(output):
            status = main(["report"])
        self.assertEqual(status, 0)
        self.assertIn("Message: Everything works!", output.getvalue())
        self.assertIn(f"Operating system: {platform.system()}", output.getvalue())
        self.assertIn(f"Python version: {platform.python_version()}", output.getvalue())

    def test_version_is_exposed_to_the_user(self):
        output = io.StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as stopped:
            main(["--version"])
        self.assertEqual(stopped.exception.code, 0)
        expected = f"soupcheck {version('danial-soupcheck-demo')}"
        self.assertEqual(output.getvalue().strip(), expected)


if __name__ == "__main__":
    unittest.main()
