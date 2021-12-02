import os
from datetime import datetime

BASE_FOLDER = "data"

def file(file):
    return f"{_get_folder(BASE_FOLDER)}/{file}"


def folder(folder):
    return _get_folder(f"{_get_folder(BASE_FOLDER)}/{folder}")


def folder_profile():
    return folder("profile")


def folder_files():
    return folder("files")


def folder_debug():
    return folder("debug")


def log(ident, *args):
    timestamp = datetime.now().strftime("%d/%m-%H:%M:%S")
    print(f'{timestamp} - {ident} - ', *args)


def now():
    return datetime.now().timestamp()


def _get_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder


def _sec_to_time(secs):
    # pretty print seconds to hour:minute:seconds
    hours = secs // 3600
    minutes = secs // 60 - hours * 60
    seconds = secs - (hours * 60 + minutes) * 60
    return hours, minutes, seconds


def pretty_short_time(secs):
    _, minutes, seconds = _sec_to_time(secs)
    return f"{minutes:02}:{seconds:02}"

