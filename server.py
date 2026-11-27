# TP SAST : diagnostic example; do not deploy without authentication.
import sqlite3
import os
import re
import ipaddress
from flask import Flask, request, abort

app = Flask(__name__)


@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchall()


@app.route("/ping")
def ping_host():
    # TP exception: only a validated, canonical IPv4 reaches the shell below.
    # nosemgrep: python.django.security.injection.command.command-injection-os-system.command-injection-os-system
    target = request.args.get("ip")
    if not re.fullmatch(r"[0-9]{1,3}(?:\.[0-9]{1,3}){3}", target or ""):
        abort(400, "Invalid IP address")
    try:
        target = str(ipaddress.IPv4Address(target))
    except ipaddress.AddressValueError:
        abort(400, "Invalid IP address")
    # Educational exception: IPv4Address rejects invalid octets and shell syntax.
    # Review this exception whenever validation or the command changes.
    # Production preference: subprocess.run with an argument list, shell=False.
    # nosemgrep: python.flask.security.injection.os-system-injection.os-system-injection, python.lang.security.dangerous-system-call.dangerous-system-call
    os.system("ping -c 1 " + target)
    return "Ping triggered"


if __name__ == "__main__":
    app.run(port=5000)
