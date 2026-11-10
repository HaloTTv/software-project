# Developer Decision Log

A local command-line tool for recording engineering decisions, why they were made, and references to issues or commits.

Requires Python 3.9 or newer. No packages to install.

```sh
python decision_log.py add "Use SQLite" "Keep records local" --ref "#42"
python decision_log.py list
python decision_log.py search sqlite
```

Search matches titles, reasoning, and references without regard to case. Entries are stored in `~/.decision-log.sqlite3`. Use `--db PATH` before the command to keep a separate log for a project.
