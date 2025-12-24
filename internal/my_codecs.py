from internal import helpers


class Codec:
    """
    Класс для представления видеокодека с его параметрами.

    Attributes:
        name (str): Имя кодека в меню.
        params (dict): Параметры рендера.
        vcodec (str): Имя кодека в ffmpeg.
    """
    codecs = list()

    def __init__(
            self,
            name: str = None,
            special_codec_parameters_flag: str = None,
            params: dict = None,
            vcodec: str = None,
    ):
        self.name = name
        self.special_codec_parameters_flag = special_codec_parameters_flag
        self.params = params
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

            "cli_flag": "-crf",  # флаг этого параметра в строке ffmpeg
            "context": "video codec options",
            # место этого параметра в строке ffmpeg (video filters, audio filters, global, special)
            "resettable": False,
            # сбрасываемое ли? Если да, то принимается "r" или "reset" чтобы не менять этот параметр при рендере
        },

        "scale": {
            "type": "handled",
            "label": "Scale",
            "help": "Resize video.",
            "cli_flag": "scale",
            "filter parameters flag": ":flags=",
            "context": "video filters",
            "resettable": True,
        },

        "scale filter": {
            "type": "choice",
            "label": "Scale Filter",
            "help": "Select scale filter (if you scaling)",
            "choices": [
                {"label": "fast bilinear (fastest, low quality)", "command_value": "fast_bilinear"},
                {"label": "bilinear (default)", "command_value": "bilinear"},
                {"label": "bicubic (slower, smoother)", "command_value": "bicubic"},
                {"label": "experimental neighbor (nearest neighbor, blocky)", "command_value": "neighbor"},
                {"label": "area (good for downscaling)", "command_value": "area"},
                {"label": "bicublin (improved bicubic, slower)", "command_value": "bicublin"},
                {"label": "lanczos (high quality, slower)", "command_value": "lanczos"},
                {"label": "spline (smooth, slow)", "command_value": "spline"},
                {"label": "gauss (gaussian filter, slow)", "command_value": "gauss"},
                {"label": "sinc (high quality, slowest)", "command_value": "sinc"}
            ],
            "cli_flag": None,
            "context": "scale filter parameter",
            "resettable": False
        },

        "fps": {
            "type": "direct",
            "label": "FPS",
            "help": "Enter desired FPS.",
            "cli_flag": "fps",
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
            "cli_flag": "-deadline",
            "context": "video codec options",
            "resettable": False
        },

        "tune": {
            "type": "choice",
            "label": "Tune (Visual quality metric)",
            "help": "Select the quality metric to optimize visual quality",
            "choices": [
                {"label": "Nothing (-1) (default)", "command_value": "-1"},
                {"label": "PSNR (0)", "command_value": "0"},
                {"label": "SSIM (1)", "command_value": "1"}
            ],
            "cli_flag": "-tune",
            "context": "video codec options",
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
            "cli_flag": "-pix_fmt",
            "context": "video codec options",
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
            "cli_flag": "-c:a",
            "context": "audio codec",
            "resettable": False
        },

        "audio bitrate": {
            "type": "direct",
            "label": "Audio Bitrate",
            "help": "Enter audio bitrate."
                    "\nUse k for kbps, M for Mbps",
            "cli_flag": "-b:a",
            "context": "audio codec options",
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
        }
    }
)

# -------------------
# SVT-AV1
# -------------------
svt_av1 = Codec(
    name="svt-av1",
    vcodec="libsvtav1",
    special_codec_parameters_flag="-svtav1-params",
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

            "cli_flag": "-crf",  # флаг этого параметра в строке ffmpeg
            "context": "video codec options",
            # место этого параметра в строке ffmpeg (video filters, audio filters, global, special)
            "resettable": False,
            # сбрасываемое ли? Если да, то принимается "r" или "reset" чтобы не менять этот параметр при рендере
        },

        "scale": {
            "type": "handled",
            "label": "Scale",
            "help": "Resize video.",
            "cli_flag": "scale",
            "filter parameters flag": ":flags=",
            "context": "video filters",
            "resettable": True,
        },

        "scale filter": {
            "type": "choice",
            "label": "Scale Filter",
            "help": "Select scale filter (if you scaling)",
            "choices": [
                {"label": "fast bilinear (fastest, low quality)", "command_value": "fast_bilinear"},
                {"label": "bilinear (default)", "command_value": "bilinear"},
                {"label": "bicubic (slower, smoother)", "command_value": "bicubic"},
                {"label": "experimental neighbor (nearest neighbor, blocky)", "command_value": "neighbor"},
                {"label": "area (good for downscaling)", "command_value": "area"},
                {"label": "bicublin (improved bicubic, slower)", "command_value": "bicublin"},
                {"label": "lanczos (high quality, slower)", "command_value": "lanczos"},
                {"label": "spline (smooth, slow)", "command_value": "spline"},
                {"label": "gauss (gaussian filter, slow)", "command_value": "gauss"},
                {"label": "sinc (high quality, slowest)", "command_value": "sinc"}
            ],
            "cli_flag": None,
            "context": "scale filter parameter",
            "resettable": False
        },

        "fps": {
            "type": "direct",
            "label": "FPS",
            "help": "Enter desired FPS.",
            "cli_flag": "fps",
            "context": "video filters",
            "resettable": True,
        },

        "preset": {
            "type": "direct",
            "label": "Preset (Compression efficiency)",
            "help": "Compression efficiency. 0-13. Lower is better."
                    "\nPreset 13 is only meant for debugging and running fast convex-hull encoding",
            "allowed": [str(i) for i in range(0, 14)],
            "cli_flag": "-preset",
            "context": "video codec options",
            "resettable": False
        },

        "tune": {
            "type": "choice",
            "label": "Tune (Visual quality metric)",
            "help": "Select the quality metric to optimize visual quality",
            "choices": [
                {"label": "Visual Quality (0)", "command_value": "0"},
                {"label": "PSNR (1) (default)", "command_value": "1"},
                {"label": "SSIM (2)", "command_value": "2"},
                {"label": "IQ (Image Quality) (3)", "command_value": "3"}
            ],
            "cli_flag": "tune",  # будет использован внутри -svtav1-params
            "context": "special codec parameters",  # SVT-специфичный параметр
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
            "cli_flag": "-pix_fmt",
            "context": "video codec options",
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
            "cli_flag": "-c:a",
            "context": "audio codec",
            "resettable": False
        },

        "audio bitrate": {
            "type": "direct",
            "label": "Audio Bitrate",
            "help": "Enter audio bitrate",
            "cli_flag": "-b:a",
            "context": "audio codec options",
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

        "uneven scale fix": {
            "type": "choice",
            "label": "Uneven Scale Fix",
            "help": "This codec needs height and width to be even numbers",
            "choices": [
                {"label": "Add 1px padding (preferable)", "command_value": helpers.ResolutionFixer.PAD},
                {"label": "Crop 1px", "command_value": helpers.ResolutionFixer.CROP},
                {"label": "Do not change", "command_value": helpers.DONT_CHANGE_STRING}
            ],
            "context": "video filters",
            "resettable": False
        }
    }
)

# -------------------
# HEVC / H.265
# -------------------
hevc265 = Codec(
    name="hevc",
    vcodec="libx265",
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

            "cli_flag": "-crf",  # флаг этого параметра в строке ffmpeg
            "context": "video codec options",
            # место этого параметра в строке ffmpeg (video filters, audio filters, global, special)
            "resettable": False,
            # сбрасываемое ли? Если да, то принимается "r" или "reset" чтобы не менять этот параметр при рендере
        },

        "scale": {
            "type": "handled",
            "label": "Scale",
            "help": "Resize video.",
            "cli_flag": "scale",
            "filter parameters flag": ":flags=",
            "context": "video filters",
            "resettable": True,
        },

        "scale filter": {
            "type": "choice",
            "label": "Scale Filter",
            "help": "Select scale filter (if you scaling)",
            "choices": [
                {"label": "fast bilinear (fastest, low quality)", "command_value": "fast_bilinear"},
                {"label": "bilinear (default)", "command_value": "bilinear"},
                {"label": "bicubic (slower, smoother)", "command_value": "bicubic"},
                {"label": "experimental neighbor (nearest neighbor, blocky)", "command_value": "neighbor"},
                {"label": "area (good for downscaling)", "command_value": "area"},
                {"label": "bicublin (improved bicubic, slower)", "command_value": "bicublin"},
                {"label": "lanczos (high quality, slower)", "command_value": "lanczos"},
                {"label": "spline (smooth, slow)", "command_value": "spline"},
                {"label": "gauss (gaussian filter, slow)", "command_value": "gauss"},
                {"label": "sinc (high quality, slowest)", "command_value": "sinc"}
            ],
            "cli_flag": None,
            "context": "scale filter parameter",
            "resettable": False
        },

        "fps": {
            "type": "direct",
            "label": "FPS",
            "help": "Enter desired FPS.",
            "cli_flag": "fps",
            "context": "video filters",
            "resettable": True,
        },

        "tune": {
            "type": "choice",
            "label": "Tune (Visual quality metric)",
            "help": "Select the quality metric to optimize visual quality",
            "choices": [
                {"label": "None", "command_value": helpers.DONT_CHANGE_STRING},
                {"label": "Grain – preserves the grain structure in old, grainy film material ",
                 "command_value": "grain"}
            ],
            "cli_flag": "-tune",
            "context": "video codec options",
            "resettable": True
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
            "cli_flag": "-preset",
            "context": "video codec options",
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
            "cli_flag": "-pix_fmt",
            "context": "video codec options",
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
            "cli_flag": "-c:a",
            "context": "audio codec",
            "resettable": False
        },

        "audio bitrate": {
            "type": "direct",
            "label": "Audio Bitrate",
            "help": "Enter audio bitrate."
                    "\nUse k for kbps, M for Mbps",
            "cli_flag": "-b:a",
            "context": "audio codec options",
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

        "uneven scale fix": {
            "type": "choice",
            "label": "Uneven Scale Fix",
            "help": "This codec needs height and width to be even numbers",
            "choices": [
                {"label": "Add 1px padding (preferable)", "command_value": helpers.ResolutionFixer.PAD},
                {"label": "Crop 1px", "command_value": helpers.ResolutionFixer.CROP},
                {"label": "Don't change", "command_value": helpers.DONT_CHANGE_STRING}
            ],
            "context": "video filters",
            "resettable": False
        }
    }
)
