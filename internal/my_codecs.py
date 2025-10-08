class Codec:
    def __init__(
            self,
            name: str = None,
            params: dict = None,
            container_defaults: list[str] = None,
            even_res: bool = True,
            vcodec: str = None,
    ):
        self.name = name
        self.params = params
        self.container_defaults = container_defaults or []
        self.even_res = even_res
        self.vcodec = vcodec

    def get_param_values(self, param: str):
        return self.params.get(param)

    def has_param(self, param: str) -> bool:
        return param in self.params

    def __repr__(self):
        return f"<Codec {self.name}>"


# -------------------
# VP9
# -------------------

vp9 = Codec(
    name="vp9",
    vcodec="libvpx-vp9",
    params={
        "crf": {
            "type": "direct",  # тип параметра.
            # direct - ввод с клавиатуры,
            # choice - выбор вариантов,
            # handled - обрабатывается собственным методом
            "label": "CRF",  # имя пункта в меню
            "help": "Quality control value (lower = better)",  # подсказка при выборе пункта меню (при вводе значения)
            "allowed": [str(i) for i in range(0, 64)],  # допустимые значения.
            # !Участвует в проверке input in allowed, а input всегда строка!

            "flag": "-crf",  # флаг этого параметра в строке ffmpeg
            "context": "global",
            # место этого параметра в строке ffmpeg (video filters, audio filters, global, special)
            "resettable": False,
            # сбрасываемое ли? Если да, то принимается "r" или "reset" чтобы не менять этот параметр при рендере
        },

        "scale": {
            "type": "handled",
            "label": "Scale",
            "help": "Resize video.",
            "context": "video filters",
            "resettable": True,
        },

        "fps": {
            "type": "direct",
            "label": "FPS",
            "help": "Enter desired FPS.",
            "flag": "-fps",
            "context": "video filters",
            "resettable": True,
        },

        "deadline": {
            "type": "choice",
            "label": "Compression efficiency (Deadline)",
            "help": "Compression efficiency (Deadline)",
            "choices": [
                {"label": "good: the default and recommended for most applications", "command_value": "good"},
                {"label": "best: recommended if you have lots of time and want the best compression efficiency",
                 "command_value": "best"},
                {"label": "realtime: recommended for live / fast encoding", "command_value": "realtime"}
            ],
            "flag": "-deadline",
            "context": "global",
            "resettable": False
        },

        "pixel_format": {
            "type": "choice",
            "label": "Pixel Format",
            "help": "Pixel Format. Specifies the color sampling and bit depth of the video (e.g. yuv420p for compatibility).",
            "choices": [
                {"label": "yuv420", "command_value": "yuv420"},
                {"label": "yuv422p", "command_value": "yuv422p"},
                {"label": "yuv444p", "command_value": "yuv444p"}
            ],
            "flag": "format",
            "context": "video filters",
            "resettable": True
        },

        "passes": {
            "type": "choice",
            "label": "Passes",
            "help": "Select encoding mode: single-pass (faster) or two-pass (better quality/size).",
            "choices": [
                {"label": "One-Pass", "command_value": "One-Pass"},
                {"label": "Two-Pass", "command_value": "Two-Pass"}
            ],
            "context": "special",
            "resettable": False
        },

        "audio codec": {
            "type": "choice",
            "label": "Audio Codec",
            "help": "Select audio codec",
            "choices": [
                {"label": "libopus", "command_value": "libopus"},
                {"label": "libvorbis", "command_value": "libvorbis"},
                {"label": "aac", "command_value": "aac"}
            ],
            "flag": "-c:a",
            "context": "audio filters",
            "resettable": False
        },

        "audio bitrate": {
            "type": "direct",
            "label": "Audio Bitrate",
            "help": "Enter audio bitrate:",
            "flag": "-b:a",
            "context": "audio filters",
            "resettable": False,
        },
        "container": {
            "type": "choice",
            "label": "Container",
            "help": "Select container:",
            "choices": [
                {"label": "webm", "command_value": "webm"},
                {"label": "mkv", "command_value": "mkv"},
                {"label": "mp4", "command_value": "mp4"}
            ],
            "context": "special",
            "resettable": False
        },

    },
    even_res=True
)

# -------------------
# SVT-AV1
# -------------------
svt_av1 = Codec(
    name="svt-av1",
    params={
        "crf": [0, 63],  # обрабатывается уникальным методом. Список содержит max и min значение.
        "scale": "__handled__",  # обрабатывается уникальным методом. Значение параметра неважно.
        "fps": "__handled__",  # обрабатывается уникальным методом. Значение параметра неважно.
        "preset": list(range(0, 10)),  # 0–9
        "pixel_format": ["yuv420p", "yuv422p", "yuv444p", "don't change"],
        "passes": ["One-Pass", "Two-Pass"],
        "container": ["mkv", "mp4", "webm"],
        "audio bitrate": [6, 510]  # обрабатывается уникальным методом. Список содержит max и min значение.
    },
    even_res=False,
    vcodec="libsvtav1"
)

# -------------------
# HEVC / H.265
# -------------------
hevc265 = Codec(
    name="hevc",
    params={
        "crf": [0, 51],  # обрабатывается уникальным методом. Список содержит max и min значение.
        "scale": "__handled__",  # обрабатывается уникальным методом. Значение параметра неважно.
        "fps": "__handled__",  # обрабатывается уникальным методом. Значение параметра неважно.
        "preset": ["ultrafast", "superfast", "veryfast", "faster", "fast",
                   "medium", "slow", "slower", "veryslow", "placebo"],
        "pixel_format": ["yuv420p", "yuv422p", "yuv444p", "don't change"],
        "passes": ["One-Pass", "Two-Pass"],
        "container": ["mp4", "mkv", "mov", "ts"],
        "audio bitrate": [6, 510]  # обрабатывается уникальным методом. Список содержит max и min значение.
    },
    even_res=True,
    vcodec="libx265"
)
