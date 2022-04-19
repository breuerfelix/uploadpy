import os
import threading
from flask import Flask, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import click
import eventlet
import eventlet.wsgi

from .utils import folder_files, log
from .yt import upload_video_locking

ALLOWED_EXTENSIONS = {"mp4", "json"}
PASSPHRASE = os.getenv("PASSPHRASE", "uploadpy")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", folder_files())


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_file(file):
    return os.path.isfile(f"{folder_files()}/{file}")


@app.route("/upload", methods=["POST"])
def upload_file():
    if not request.stream:
        return "Stream not found", 400

    if "filename" not in request.headers:
        return "Header: 'filename' not found", 400

    filename = request.headers["filename"]

    if not allowed_file(filename) and \
        secure_filename(filename) != filename:
        return "filename is not allowed", 400

    FileStorage(request.stream).save(
        os.path.join(app.config["UPLOAD_FOLDER"], filename)
    )

    return "done", 200


@app.route("/youtube", methods=["POST"])
def upload_youtube():
    if not request.is_json:
        return "not json", 400

    data = request.get_json()
    if data is None:
        return "failed to parse json", 400

    if not "ident" in data:
        return "missing ident", 400

    if not "passphrase" in data:
        return "missing passphrase", 400

    if PASSPHRASE != data["passphrase"]:
        return "error", 400

    ident = data["ident"]
    log(ident, "request for upload")

    if not is_file(f"{ident}.json") or not is_file(f"{ident}.mp4"):
        return "files not uploaded for this ident", 400

    threading.Thread(
        target=upload_video_locking,
        args=[ident],
        daemon=True,
    ).start()

    return "done", 200


@app.route("/health", methods=["GET"])
def health():
    return "still breathing", 200


@click.group()
def cli():
    pass


@cli.command()
def start():
    port = os.getenv("PORT", 80)
    eventlet.wsgi.server(eventlet.listen(('', int(port))), app)


@cli.command()
def test():
    print("imports are working")


if __name__ == "__main__":
    app.run(debug = True)

