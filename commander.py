import os

import helpers


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
        container = self.settings.get("container")
        crf = self.settings.get("crf")
        preset = self.settings.get("preset")
        fps = self.settings.get("fps")
        pixel_format = self.settings.get("pixel_format")
        passes = self.settings.get("passes")
        audio_bitrate = int(self.settings.get("audio bitrate"))

        # Видеофильтры
        vf_list = []

        scale = self.settings.get("scale")
        if scale and scale != "don't change":
            vf_list.append(f"scale={scale}")

        scale_fix = self.settings.get("scale_fix")
        if scale_fix:
            if scale_fix == "pad":
                scale_fix = helpers.ResolutionFixer.pad()
                vf_list.append(scale_fix)

            if scale_fix == "crop":
                scale_fix = helpers.ResolutionFixer.crop()
                vf_list.append(scale_fix)

        if fps and fps != "don't change":
            vf_list.append(f"fps={fps}")
        if pixel_format and pixel_format != "don't change":
            vf_list.append(f"format={pixel_format}")

        vf = "-vf \"" + ",".join(vf_list) + "\"" if vf_list else ""

        output_file = os.path.join(output_dir, f"{filename}_{self.codec.name}_q{crf}")

        vcodec = self.codec.vcodec
        acodec = self.codec.acodec

        if passes == "One-Pass":
            cmd = (
                f'ffmpeg -y -i "{file}" {vf} -c:v {vcodec} '
                f'-preset {str(preset)} -crf {str(crf)} '
                f'-c:a {acodec} -b:a {audio_bitrate}k "{output_file}_1pass.{container}"'
            )
        elif passes == "Two_Pass":
            nol = "NUL" if os.name == "nt" else "/dev/null"
            cmd = (
                f'ffmpeg -y -i "{file}" {vf} -c:v {vcodec} '
                f'-preset {str(preset)} -crf {str(crf)} -pass 1 -an -f null {nol} && '
                f'ffmpeg -y -i "{file}" {vf} -c:v {vcodec} '
                f'-preset {str(preset)} -crf {str(crf)} -pass 2 '
                f'-c:a {acodec} -b:a {audio_bitrate}k "{output_file}_2pass.{container}"'
            )
        else:
            raise ValueError(f"Passes should be one of 'One-Pass', 'Two-Pass'")
        return cmd
