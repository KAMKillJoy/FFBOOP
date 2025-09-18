class Codec:
    def __init__(
            self,
            name: str,
            params: dict,
            container_defaults: list[str] = None,
            even_res: bool = True,
            vcodec: str = None,
            acodec: str = None,
    ):
        self.name = name
        self.params = params
        self.container_defaults = container_defaults or []
        self.even_res = even_res
        self.vcodec = vcodec
        self.acodec = acodec

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
    params={
        "crf": [0, 63],  # обрабатывается уникальным методом. Список содержит max и min значение.
        "scale": "",  # обрабатывается уникальным методом. Значение параметра неважно.
        "fps": "",  # обрабатывается уникальным методом. Значение параметра неважно.
        "preset": ["realtime", "good", "best"],
        "pixel_format": ["yuv420p", "yuv422p", "yuv444p", "don't change"],
        "passes": ["One-Pass", "Two-Pass"],
        "container": ["webm", "mkv", "mp4"],
        "audio bitrate": [6, 510]  # обрабатывается уникальным методом. Список содержит max и min значение.
    },
    even_res=True,
    vcodec="libvpx-vp9",
    acodec="libopus"
)

# -------------------
# SVT-AV1
# -------------------
svt_av1 = Codec(
    name="svt-av1",
    params={
        "crf": [0, 63],
        "scale": None,
        "fps": None,
        "preset": list(range(0, 10)),  # 0–9
        "pixel_format": ["yuv420p", "yuv422p", "yuv444p", "don't change"],
        "passes": ["One-Pass", "Two-Pass"],
        "container": ["mkv", "mp4", "webm"],
        "audio bitrate": [6, 510]
    },
    even_res=False,
    vcodec="libsvtav1",
    acodec="libopus"
)

# -------------------
# HEVC / H.265
# -------------------
hevc265 = Codec(
    name="hevc",
    params={
        "crf": [0, 51],
        "scale": None,
        "fps": None,
        "preset": ["ultrafast", "superfast", "veryfast", "faster", "fast",
                   "medium", "slow", "slower", "veryslow", "placebo"],
        "pixel_format": ["yuv420p", "yuv422p", "yuv444p", "don't change"],
        "passes": ["One-Pass", "Two-Pass"],
        "container": ["mp4", "mkv", "mov", "ts"],
        "audio bitrate": [6, 510]
    },
    even_res=True,
    vcodec="libx265",
    acodec="libopus"
)
