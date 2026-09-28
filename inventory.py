import os

hosts = [
    ("steamdeck.local", {
        "ssh_user": "deck",
    }),
    ("steammachine.local", {
        "ssh_user": "deck",
        "otlp_endpoint": "https://ingress.europe-west4.gcp.dash0.com:4317",
        "otlp_token": os.environ['OTLP_TOKEN'],
    }),
]