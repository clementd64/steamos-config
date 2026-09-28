import json
import os
import re
from urllib.request import Request, urlopen

from pyinfra import host
from pyinfra.api import deploy
from pyinfra.operations import files, systemd


VERSION = "0.0.8"
ASSET_NAME = f"opentelemetry-gpu-collector-{VERSION}-linux-amd64"
RELEASE_API_URL = f"https://api.github.com/repos/openlit/openlit/releases/tags/otel-gpu-collector-{VERSION}"
RELEASE_URL = (
    "https://github.com/openlit/openlit/releases/download/"
    f"otel-gpu-collector-{VERSION}/{ASSET_NAME}"
)


def release_sha256():
    request = Request(
        RELEASE_API_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "steamos-config",
        },
    )
    with urlopen(request, timeout=15) as response:
        release = json.load(response)

    for asset in release["assets"]:
        if asset["name"] == ASSET_NAME:
            digest = asset.get("digest", "")
            if not re.fullmatch(r"sha256:[0-9a-fA-F]{64}", digest):
                raise ValueError(f"GitHub release asset {ASSET_NAME} has no valid SHA256 digest")
            return digest.removeprefix("sha256:")

    raise ValueError(f"GitHub release asset {ASSET_NAME} was not found")


@deploy("Install OpenTelemetry GPU Collector")
def install_otel_gpu_collector():
    files.directory(
        name="Ensure user binary directory exists",
        path=".local/bin",
    )
    files.directory(
        name="Ensure user systemd directory exists",
        path=".config/systemd/user",
    )

    files.download(
        name=f"Download OpenTelemetry GPU Collector {VERSION}",
        src=RELEASE_URL,
        dest=".local/bin/opentelemetry-gpu-collector",
        sha256sum=release_sha256(),
        mode="0755",
    )

    files.template(
        name="Install OpenTelemetry GPU Collector user service",
        src="templates/otel-gpu-collector.service.j2",
        dest=".config/systemd/user/otel-gpu-collector.service",
        mode="0600",
        endpoint=host.data.get("otlp_endpoint"),
        token=host.data.get("otlp_token"),
    )

    systemd.service(
        name="Enable and start OpenTelemetry GPU Collector",
        service="otel-gpu-collector",
        daemon_reload=True,
        enabled=True,
        restarted=True,
        running=True,
        user_mode=True,
    )
