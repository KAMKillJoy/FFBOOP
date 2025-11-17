class Codec:
    """
    Класс для представления видеокодека с его параметрами.

    Attributes:
        name (str): Имя кодека в меню.
        params (dict): Параметры рендера.
        even_res (bool): Флаг, указывающий, должны ли значения высоты и ширины быть чётными. Уточни в документации кодека
        vcodec (str): Имя кодека в ffmpeg.
    """
    codecs = list()

    def __init__(
            self,
            name: str = None,
            params: dict = None,
            even_res: bool = False,
            vcodec: str = None,
    ):
        self.name = name
        self.params = params
        self.even_res = even_res
        self.vcodec = vcodec

        Codec.codecs.append(self)  # составление списка поддерживаемых кодеков. Хранит сами экземляры.

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
    even_res=True,
    params={
        "crf": {
            "type": "direct",  # тип параметра.
            # direct - ввод с клавиатуры,
            # choice - выбор вариантов,
            # handled - ничего конкретного не значит, просто подсказка, что обрабатывается собственным методом.
            "label": "CRF",  # имя пункта в меню
            "help": "Quality control value. 0-63 (lower = better). 35 is good.",
            # подсказка при выборе пункта меню (при вводе значения)
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
            "flag": "scale",
            "context": "video filters",
            "resettable": True,
        },

        "fps": {
            "type": "direct",
            "label": "FPS",
            "help": "Enter desired FPS.",
            "flag": "fps",
            "context": "video filters",
            "resettable": True,
        },

        "deadline": {
            "type": "choice",
            "label": "Deadline (Compression efficiency)",
            "help": "Deadline (Compression efficiency)",
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
                {"label": "yuv420p (8 bit. Most compatible)", "command_value": "yuv420p"},
                {"label": "yuv422p (10 bit)", "command_value": "yuv422p"},
                {"label": "yuv444p (12 bit)", "command_value": "yuv444p"}
            ],
            "flag": "-pix_fmt",
            "context": "global",
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
            "context": "global",
            "resettable": False
        },

        "audio bitrate": {
            "type": "direct",
            "label": "Audio Bitrate",
            "help": "Enter audio bitrate."
                    "\nUse k for kbps, M for Mbps",
            "flag": "-b:a",
            "context": "global",
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

    }
)

# -------------------
# SVT-AV1
# -------------------
svt_av1 = Codec(
    name="svt-av1",
    vcodec="libsvtav1",
    even_res=True,
    params={
        "crf": {
            "type": "direct",  # тип параметра.
            # direct - ввод с клавиатуры,
            # choice - выбор вариантов,
            # handled - ничего конкретного не значит, просто подсказка, что обрабатывается собственным методом.
            "label": "CRF",  # имя пункта в меню
            "help": "Quality control value. 0-63 (lower = better). 23 is good.",
            # подсказка при выборе пункта меню (при вводе значения)
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
            "flag": "scale",
            "context": "video filters",
            "resettable": True,
        },

        "fps": {
            "type": "direct",
            "label": "FPS",
            "help": "Enter desired FPS.",
            "flag": "fps",
            "context": "video filters",
            "resettable": True,
        },

        "preset": {
            "type": "direct",
            "label": "Preset (Compression efficiency)",
            "help": "Compression efficiency. 0-13. Lower is better."
                    "\nPreset 13 is only meant for debugging and running fast convex-hull encoding",
            "allowed": [str(i) for i in range(0, 14)],
            "flag": "-preset",
            "context": "global",
            "resettable": False
        },

        "pixel_format": {
            "type": "choice",
            "label": "Pixel Format",
            "help": "Pixel Format. Specifies the color sampling and bit depth of the video (e.g. yuv420p for compatibility).",
            "choices": [
                {"label": "yuv420p (8 bit. Most compatible)", "command_value": "yuv420p"},
                {"label": "yuv422p (10 bit)", "command_value": "yuv422p"},
                {"label": "yuv444p (12 bit)", "command_value": "yuv444p"}
            ],
            "flag": "-pix_fmt",
            "context": "global",
            "resettable": True
        },

        "audio codec": {
            "type": "choice",
            "label": "Audio Codec",
            "help": "Enter audio bitrate."
                    "\nUse k for kbps, M for Mbps",

            "choices": [
                {"label": "libopus", "command_value": "libopus"},
                {"label": "libvorbis", "command_value": "libvorbis"},
                {"label": "aac", "command_value": "aac"}
            ],
            "flag": "-c:a",
            "context": "global",
            "resettable": False
        },

        "audio bitrate": {
            "type": "direct",
            "label": "Audio Bitrate",
            "help": "Enter audio bitrate",
            "flag": "-b:a",
            "context": "global",
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

    }

)

# -------------------
# HEVC / H.265
# -------------------
hevc265 = Codec(
    name="hevc",
    vcodec="libx265",
    even_res=True,
    params={
        "crf": {
            "type": "direct",  # тип параметра.
            # direct - ввод с клавиатуры,
            # choice - выбор вариантов,
            # handled - ничего конкретного не значит, просто подсказка, что обрабатывается собственным методом.
            "label": "CRF",  # имя пункта в меню
            "help": "Quality control value. 0-52 (lower = better). 23 is good.",
            # подсказка при выборе пункта меню (при вводе значения)
            "allowed": [str(i) for i in range(0, 52)],  # допустимые значения для проверки if in allowed
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
            "flag": "scale",
            "context": "video filters",
            "resettable": True,
        },

        "fps": {
            "type": "direct",
            "label": "FPS",
            "help": "Enter desired FPS.",
            "flag": "fps",
            "context": "video filters",
            "resettable": True,
        },

        "preset": {
            "type": "choice",
            "label": "Preset (Compression efficiency)",
            "help": "Compression efficiency",
            "choices": [
                {"label": "ultrafast", "command_value": "ultrafast"},
                {"label": "superfast", "command_value": "superfast"},
                {"label": "veryfast", "command_value": "veryfast"},
                {"label": "faster", "command_value": "faster"},
                {"label": "fast", "command_value": "fast"},
                {"label": "medium", "command_value": "medium"},
                {"label": "slow", "command_value": "slow"},
                {"label": "slower", "command_value": "slower"},
                {"label": "veryslow", "command_value": "veryslow"},
                {"label": "placebo", "command_value": "placebo"}
            ],
            "flag": "-preset",
            "context": "global",
            "resettable": False
        },

        "pixel_format": {
            "type": "choice",
            "label": "Pixel Format",
            "help": "Pixel Format. Specifies the color sampling and bit depth of the video (e.g. yuv420p for compatibility).",
            "choices": [
                {"label": "yuv420p (8 bit. Most compatible)", "command_value": "yuv420p"},
                {"label": "yuv422p (10 bit)", "command_value": "yuv422p"},
                {"label": "yuv444p (12 bit)", "command_value": "yuv444p"}
            ],
            "flag": "-pix_fmt",
            "context": "global",
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
            "context": "global",
            "resettable": False
        },

        "audio bitrate": {
            "type": "direct",
            "label": "Audio Bitrate",
            "help": "Enter audio bitrate."
                    "\nUse k for kbps, M for Mbps",
            "flag": "-b:a",
            "context": "global",
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

    }

)
