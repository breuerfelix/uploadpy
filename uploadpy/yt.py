import os
import json
from threading import Lock
from .ytbrowser import upload
from .ytapi import get_api, update, dump_token
from .utils import folder_files

LOCK = Lock()

def delete_files(ident):
    extensions = [".mp4", ".json"]
    for ext in extensions:
        folder = folder_files()
        filename = f"{folder}/{ident}{ext}"
        if os.path.exists(filename):
            os.remove(filename)


def upload_video(ident):
    id = upload(ident)
    if not id:
        print("Video failed to upload")
        return

    folder = folder_files()
    filename = f"{folder}/{ident}.json"
    with open(filename, "r") as f:
        raw = f.read()

    meta = json.loads(raw)
    snippet = meta["snippet"]

    yt, creds = get_api()
    done = update(yt, id, snippet["title"], snippet["description"], snippet["tags"])
    if not done:
        print("Error: Could not update video")

    dump_token(creds)
    print(f"Video meta data for {snippet['title']} changed")

    delete_files(ident)
    print(f"Deleted files for ident: {ident}")


def upload_video_locking(ident):
    LOCK.acquire()
    try:
        upload_video(ident)
    except Exception as e:
        print("ERROR UPLOADING")
        print(e)
    finally:
        LOCK.release()

