import os

from internal import helpers
from internal.my_codecs import Codec


class Commander:
    def __init__(self, codec: Codec, settings: dict):
        """
        codec    - объект Codec
        settings - словарь с выбранными параметрами из Menu
        """
        self.codec = codec
        self.settings = settings

    def __parse_params(self, context) -> dict:
        params = self.codec.params
        return {key: value
                for key, value in params.items() if isinstance(value, dict) and value.get("context") == context}

    def __build_options_string(self,
                               context: str,
                               option_flag: str,
                               separator: str,
                               exclude: tuple[str, ...] = ()
                               ) -> str:

        o_params = self.__parse_params(context)
        params_list = []
        for key, value in o_params.items():
            val = self.settings.get(key)
            if key in exclude:
                continue
            if not val or val == helpers.DONT_CHANGE_STRING:
                continue
            flag = value.get("flag")
            if not flag:
                continue
            params_list.append(f"{flag}{separator}{val}")

        o_string = f'{option_flag} "{",".join(params_list)}"' if params_list else ""
        return o_string

    def build_ffmpeg_command(self, file: str, output_dir) -> str:
        """
        Генерация ffmpeg команды для одного файла с учётом настроек.
        Универсальная для любого кодека, использует codec.vcodec/acodec.
        """

        filename, ext = os.path.splitext(os.path.basename(file))
        param_for_name = f'_q{self.settings.get("crf")}'  # магические литералы, может исправлю.
        passes = self.settings.get("passes")
        container = self.settings.get("container")

        helpers.ResolutionFixer.replace_resolution_fixer(self.settings)

        video_filters = self.__build_options_string("video filters", "-vf", "=")
        audio_filters = self.__build_options_string("audio filters", "-af", "=")
        global_options = self.__build_options_string("global", "", " ")

        output_file = os.path.join(output_dir, f'{filename}_{self.codec.name}{param_for_name}')

        if passes not in ("One-Pass", "Two-Pass", None):
            raise ValueError(f"Passes should be one of 'One-Pass', 'Two-Pass'")

        elif passes in ("One-Pass", None):
            cmd = (
                f'ffmpeg -y '
                f'-i "{file}" '
                f'{video_filters} {audio_filters} {global_options} '
                f'"{output_file}_1pass.{container}"'
            )
        else:  # passes == "Two-Pass"
            global_options_wo_audio = self.__build_options_string("global", "", " ",
                                                                  helpers.FIRST_PASS_SKIP_PARAMS)
            cmd1 = (f'ffmpeg -y '
                    f'-i "{file}" '
                    f'{video_filters} {global_options_wo_audio} '
                    f'-pass 1 -an -f null {helpers.os_adapter.NULL_DEVICE} '
                    )

            cmd2 = (f'ffmpeg -y '
                    f'-i "{file}" '
                    f'{video_filters} {audio_filters} {global_options} '
                    f'"{output_file}_2pass.{container}"'
                    )

            cmd = f'{cmd1} && {cmd2}'
        return cmd
