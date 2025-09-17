class Codec:
    def __init__(
            self,
            name: str,
            params: dict,
            container_defaults: list[str] = None,
            even_res: bool = True
    ):
        self.name = name
        self.params = params
        self.container_defaults = container_defaults or []
        self.even_res = even_res

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
        "crf": range(0, 64),  # 0–63
        "scale": None,  # свободный ввод
        "fps": None,  # свободный ввод
        "preset": ["realtime", "good", "best"],
        "pixel_format": ["yuv420p", "yuv422p", "yuv444p"],
        "passes": [1, 2],  # One-Pass / Two-Pass
        "container": ["webm", "mkv"]
    },
    even_res=True
)

# -------------------
# SVT-AV1
# -------------------
svt_av1 = Codec(
    name="svt-av1",
    params={
        "crf": range(0, 64),
        "scale": None,
        "fps": None,
        "preset": list(range(0, 10)),  # 0–9
        "pixel_format": ["yuv420p", "yuv422p", "yuv444p"],
        "passes": [1, 2],
        "container": ["mkv", "mp4", "webm"]
    },
    even_res=False
)

# -------------------
# HEVC / H.265
# -------------------
hevc265 = Codec(
    name="hevc",
    params={
        "crf": range(0, 52),  # libx265 обычно 0–51
        "scale": None,
        "fps": None,
        "preset": ["ultrafast", "superfast", "veryfast", "faster", "fast",
                   "medium", "slow", "slower", "veryslow", "placebo"],
        "pixel_format": ["yuv420p", "yuv422p", "yuv444p"],
        "passes": [1, 2],
        "container": ["mp4", "mkv", "mov", "ts"]
    },
    even_res=True
)
