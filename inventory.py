import os

hosts = [
    ("steamdeck.local", {
        "ssh_user": "deck",
        "uptrace_dsn": os.environ.get("UPTRACE_DSN_STEAMDECK"),
    }),
    ("steammachine.local", {
        "ssh_user": "deck",
        "uptrace_dsn": os.environ.get("UPTRACE_DSN_STEAMMACHINE"),
    }),
]