import json
import os
import shutil
import subprocess
import sys

from internal import my_codecs

DONT_CHANGE_STRING = "don't change"
"""
Это значение параметра, которое присваивается параметру кодека, если его не надо менять. 
Оно же отображается в консольном меню
"""


class ResolutionFixer:
    PAD = "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2"
    CROP = "crop=trunc(iw/2)*2:trunc(ih/2)*2"


script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
options_path = os.path.join(script_dir, "options.json")


def load_options(codec_name: str) -> dict:
    if not os.path.exists(options_path):
        create_options_json()

    with open(options_path, "r", encoding="utf-8") as f:
        return json.load(f).get(codec_name, {})


def create_options_json():
    """
    Создаёт options_json с базовыми значениями кодеков
    """
    defaults = {
        "vp9": {
            "crf": 35,
            "scale": DONT_CHANGE_STRING,
            "preset": "good",
            "fps": DONT_CHANGE_STRING,
            "pixel_format": "yuv420p",
            "passes": "Two-Pass",
            "container": "webm",
            "audio bitrate": 128
        },
        "svt-av1": {
            "crf": 28,
            "scale": DONT_CHANGE_STRING,
            "preset": "8",
            "fps": DONT_CHANGE_STRING,
            "pixel_format": "yuv420p",
            "passes": "Two-Pass",
            "container": "mkv",
            "audio bitrate": 128
        },
        "hevc": {
            "crf": 23,
            "scale": DONT_CHANGE_STRING,
            "preset": "medium",
            "fps": DONT_CHANGE_STRING,
            "pixel_format": "yuv420p",
            "passes": "Two-Pass",
            "container": "mp4",
            "audio bitrate": 128
        }
    }

    with open(options_path, "w", encoding="utf-8") as f:
        json.dump(defaults, f, indent=4)
    print(f"Created options.json at {options_path}")


def supported_codecs() -> list:
    """
    Возвращает список объектов Codec, доступных в my_codecs.
    """
    return [
        obj for name, obj in vars(my_codecs).items()
        if isinstance(obj, my_codecs.Codec)
    ]


class PlatformAdapter:
    NULL_DEVICE: str

    def set_terminal_title(self, title: str):
        raise NotImplemented

    def open_directory(self, dest: str):
        raise NotImplemented

    def clear_screen(self):
        raise NotImplemented


class WindowsAdapter(PlatformAdapter):
    NULL_DEVICE = "NUL"

    def set_terminal_title(self, title: str):
        os.system(f"title {title}")

    def open_directory(self, dest: str):
        os.startfile(dest)

    def clear_screen(self):
        os.system("cls")


class PosixAdapter(PlatformAdapter):
    NULL_DEVICE = "/dev/null"

    def set_terminal_title(self, title: str):
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

    def open_directory(self, dest: str):
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.run([opener, dest])

    def clear_screen(self):
        os.system("clear")


if os.name == "nt":
    os_adapter = WindowsAdapter()
else:
    os_adapter = PosixAdapter()


def check_ffmpeg_installed():
    if shutil.which("ffmpeg") is None:
        print("FFmpeg не найден. Установите ffmpeg и убедитесь, что он доступен в PATH.")
        sys.exit(1)