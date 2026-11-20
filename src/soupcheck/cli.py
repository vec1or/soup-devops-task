"""Print a small report using a file shipped inside the installed package."""

import argparse
import json
import platform
from importlib.metadata import version
from importlib.resources import files


DISTRIBUTION_NAME = "danial-soupcheck-demo"


def make_report() -> str:
    """Read package data and describe the current Python environment."""
    resource = files("soupcheck").joinpath("message.json")
    data = json.loads(resource.read_text(encoding="utf-8"))
    return "\n".join(
        [
            f"Application version: {version(DISTRIBUTION_NAME)}",
            f"Python version: {platform.python_version()}",
            f"Operating system: {platform.system()}",
            f"Message: {data['message']}",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    """Handle command-line arguments and return an exit status."""
    parser = argparse.ArgumentParser(
        prog="soupcheck", description="Print a small environment report."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version(DISTRIBUTION_NAME)}"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("report", help="Show versions, the OS, and a packaged message.")
    args = parser.parse_args(argv)
    if args.command == "report":
        print(make_report())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
