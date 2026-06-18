import os
from flask import Flask, jsonify

app = Flask(__name__)

HOST_PATH = os.getenv("PATH_TO_MONITOR", "/storage")
CONTAINER_PATH = "/storage"
UNIT = os.getenv("UNIT", "TB").upper()

SUBTITLE = os.getenv("SUBTITLE", "")
SHOW_SUBTITLE = os.getenv("SHOW_SUBTITLE", "true").lower() != "false"

UNITS = {
    "B": 1,
    "KB": 1000,
    "MB": 1000 ** 2,
    "GB": 1000 ** 3,
    "TB": 1000 ** 4,
}


def format_size(bytes_value: int) -> str:
    divisor = UNITS.get(UNIT, UNITS["TB"])
    value = bytes_value / divisor
    return f"{value:.2f} {UNIT}"


@app.route("/")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/storage")
def storage_stats():
    stats = os.statvfs(CONTAINER_PATH)

    total = stats.f_blocks * stats.f_frsize
    free = stats.f_bavail * stats.f_frsize
    used = total - free

    used_percent = round((used / total) * 100, 1) if total else 0
    free_percent = round((free / total) * 100, 1) if total else 0

    return jsonify({
        "subtitle": SUBTITLE,
        "show_subtitle": SHOW_SUBTITLE,
        "host_path": HOST_PATH,
	"container_path": CONTAINER_PATH,
        "unit": UNIT,
        "total_bytes": total,
        "used_bytes": used,
        "free_bytes": free,
        "total": format_size(total),
        "used": format_size(used),
        "free": format_size(free),
        "used_percent": used_percent,
        "free_percent": free_percent,
    })
