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
                               kv_separator: str,
                               join_sep: str,
                               exclude: tuple[str, ...] = ()
                               ) -> str:
        """
        Формирует строку опций ffmpeg для конкретного контекста, готовую для вставки в команду.

        Аргументы:
            context (str): Контекст настроек для обработки
                (например, "video filters", "audio filters" или "global").
            option_flag (str): Флаг, который будет добавлен перед опциями
                (например, "-vf" для видеофильтров). Можно оставить пустым для глобальных опций.
            kv_separator (str): Разделитель между флагом и его значением
                (например, "=" для "-crf=21" или пробел для "-crf 21").
            join_sep (str): Разделитель между несколькими опциями в результирующей строке
                (например, "," для фильтров или пробел для глобальных опций).
            exclude (tuple[str, ...], optional): Ключи настроек, которые нужно исключить из результата. По умолчанию ().

        Возвращает:
            str: Сформированная часть строки командной строки с опциями для ffmpeg.
                 Если нет валидных опций — возвращается пустая строка.
        """

        o_params = self.__parse_params(context)
        params_list = []
        for key, value in o_params.items():
            val = self.settings.get(key)
            if key in exclude:
                continue
            if not val or val == helpers.DONT_CHANGE_STRING:
                continue
            flag = value.get("flag")
            if flag:
                params_list.append(f"{flag}{kv_separator}{val}")
            else:
                params_list.append(f"{val}")

        o_string = f'{option_flag} {f"{join_sep}".join(params_list)}' if params_list else ""
        return o_string.strip()

    def __build_video_filters_substr(self):
        video_filters = self.__build_options_string("video filters", "-vf", "=", ",")
        return video_filters

    def __build_audio_filters_substr(self):
        audio_filters = self.__build_options_string("audio filters", "-af", "=", ",")
        return audio_filters

    def __build_global_filters_substr(self):
        global_options = self.__build_options_string("global", "", " ", " ")
        return global_options

    def build_ffmpeg_command(self, file: str, output_dir) -> str:
        """
        Генерация ffmpeg команды для одного файла с учётом настроек.
        """

        filename, ext = os.path.splitext(os.path.basename(file))
        param_for_name = f'_q{self.settings.get("crf")}'  # магические литералы, может исправлю.
        passes = self.settings.get("passes")
        container = self.settings.get("container")

        video_filters = self.__build_video_filters_substr()
        audio_filters = self.__build_audio_filters_substr()
        global_options = self.__build_global_filters_substr()

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
