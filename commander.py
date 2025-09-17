def build_ffmpeg_command(self, file: str) -> str:
    """
    Генерация ffmpeg команды для одного файла с учётом настроек.
    """
    import os

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    if "output" not in os.listdir(os.path.dirname(__file__)):
        os.mkdir(output_dir)

    filename, ext = os.path.splitext(os.path.basename(file))
    container = self.settings.get("container", "webm")
    crf = self.settings.get("crf", 35)
    preset = self.settings.get("preset", "good")
    fps = self.settings.get("fps", None)
    pixel = self.settings.get("pixel", None)
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

    output_file = os.path.join(output_dir, f"{filename}_vp9_q{crf}")

    if passes == "One-Pass":
        cmd = f'ffmpeg -y -i "{file}" {vf} -c:v libvpx-vp9 -b:v 0 -deadline {preset} -crf {crf} -row-mt 1 -c:a libopus -b:a 128k "{output_file}_1pass.{container}"'
    else:  # Two-Pass
        nol = "NUL" if os.name == "nt" else "/dev/null"
        cmd = (
            f'ffmpeg -y -i "{file}" {vf} -c:v libvpx-vp9 -b:v 0 -deadline {preset} -crf {crf} -row-mt 1 '
            f'-pass 1 -an -f null {nol} && '
            f'ffmpeg -y -i "{file}" {vf} -c:v libvpx-vp9 -b:v 0 -deadline {preset} -crf {crf} -row-mt 1 '
            f'-pass 2 -c:a libopus -b:a 128k "{output_file}_2pass.{container}"'
        )
    return cmd
