# commander.py
import os

class Commander:
    def __init__(self, codec, settings: dict):
        """
        codec    - объект Codec
        settings - словарь с выбранными параметрами из Menu
        """
        self.codec = codec
        self.settings = settings

    def build_ffmpeg_command(self, file: str, output_dir) -> str:
        """
        Генерация ffmpeg команды для одного файла с учётом настроек.
        Универсальная для любого кодека, использует codec.vcodec/acodec.
        """

        filename, ext = os.path.splitext(os.path.basename(file))
        container = self.settings.get("container", "mp4")
        crf = self.settings.get("crf", 35)
        preset = self.settings.get("preset", "medium")
        fps = self.settings.get("fps", None)
        pixel = self.settings.get("pixel_format", None)
        passes = self.settings.get("passes", "Two-Pass")

        # Видеофильтры
        vf_list = []

        scale = self.settings.get("scale")
        if scale:
            vf_list.append(f"scale={scale}")

        scale_fix = self.settings.get("scale_fix")
        if scale_fix:
            vf_list.append(scale_fix)

        if fps and fps != "don't change":
            vf_list.append(f"fps={fps}")
        if pixel and pixel != "don't change":
            vf_list.append(f"format={pixel}")

        vf = "-vf \"" + ",".join(vf_list) + "\"" if vf_list else ""

        output_file = os.path.join(output_dir, f"{filename}_{self.codec.name}_q{crf}")

        vcodec = self.codec.vcodec
        acodec = self.codec.acodec

        if passes == "One-Pass" or passes == 1:
            cmd = (
                f'ffmpeg -y -i "{file}" {vf} -c:v {vcodec} '
                f'-preset {preset} -crf {crf} '
                f'-c:a {acodec} -b:a 128k "{output_file}_1pass.{container}"'
            )
        else:  # Two-Pass
            nol = "NUL" if os.name == "nt" else "/dev/null"
            cmd = (
                f'ffmpeg -y -i "{file}" {vf} -c:v {vcodec} '
                f'-preset {preset} -crf {crf} -pass 1 -an -f null {nol} && '
                f'ffmpeg -y -i "{file}" {vf} -c:v {vcodec} '
                f'-preset {preset} -crf {crf} -pass 2 '
                f'-c:a {acodec} -b:a 128k "{output_file}_2pass.{container}"'
            )

        return cmd
