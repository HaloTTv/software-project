"""Local developer decision log. Run with --help for usage."""
import argparse
from contextlib import closing
from pathlib import Path
import sqlite3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path.home() / ".decision-log.sqlite3")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Record a decision and its reasoning")
    add.add_argument("title")
    add.add_argument("reason")
    add.add_argument("--ref", default="", help="Issue URL, commit hash, or other reference")
    commands.add_parser("list", help="List decisions newest first")
    search = commands.add_parser("search", help="Search titles, reasoning, and references")
    search.add_argument("query")
    args = parser.parse_args()

    try:
        with closing(sqlite3.connect(args.db)) as db, db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS decisions (
                    id INTEGER PRIMARY KEY,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    title TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    reference TEXT NOT NULL
                )
            """)
            if args.command == "add":
                title, reason = args.title.strip(), args.reason.strip()
                if not title or not reason:
                    parser.error("title and reason must contain text")
                result = db.execute(
                    "INSERT INTO decisions (title, reason, reference) VALUES (?, ?, ?)",
                    (title, reason, args.ref.strip()),
                )
                print(f"Added decision #{result.lastrowid}")
                return

            rows = db.execute("""
                SELECT id, created_at, title, reason, reference
                FROM decisions ORDER BY id DESC
            """)
            query = args.query.casefold() if args.command == "search" else ""
            found = False
            for decision_id, created_at, title, reason, reference in rows:
                if query and not any(query in value.casefold() for value in (title, reason, reference)):
                    continue
                found = True
                print(f"#{decision_id} [{created_at} UTC] {title}\n  {reason}")
                if reference:
                    print(f"  Reference: {reference}")
                print()
            if not found:
                print("No matching decisions.")
    except sqlite3.Error as error:
        parser.exit(1, f"Decision log error: {error}\n")


if __name__ == "__main__":
    main()
