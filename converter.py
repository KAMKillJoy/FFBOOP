#!/usr/bin/env python3

import argparse
import os
import subprocess
from datetime import datetime

from internal import commander, helpers
from internal.menu import Menu

helpers.check_ffmpeg_installed()


def parse_args():
    parser = argparse.ArgumentParser(description="FF8MBOOP - batch video converter")
    parser.add_argument("files", nargs="*", help="Input video files, separated by space")
    parser.add_argument("--codec", type=str, help="Codec to use (e.g., h264, hevc, vp9)")
    parser.add_argument("--skip-menu", action="store_true", help="Skip interactive menu")
    parser.add_argument("--output-dir", type=str, help="Override output directory")
    return parser.parse_args()


def main(preselected_codec=None, skip_menu: bool = False):
    helpers.os_adapter.set_terminal_title("FF8MBOOP")
    args = parse_args()

    codecs = helpers.supported_codecs()

    files = args.files
    '''if not files:
        print("No input files. Drag & drop video files onto this script.")
        return'''

    # Выбор кодека
    if preselected_codec:
        codec = preselected_codec
    elif args.codec:
        codec = next((c for c in codecs if c.name.lower() == args.codec.lower()), None)
        if not codec:
            print(f"Codec '{args.codec}' not supported.")
            if not (skip_menu or args.skip_menu):
                codec = Menu.choose_codec_menu(codecs)
            else:
                print("No valid codec selected, exiting.")
                return
    else:
        if not (skip_menu or args.skip_menu):
            codec = Menu.choose_codec_menu(codecs)
        else:
            print("No valid codec selected, exiting.")
            return

    helpers.os_adapter.set_terminal_title(f"FF8MBOOP - {codec.name}")

    # Загружаем стандартные значения
    settings = helpers.load_options(codec.name)

    if codec.even_res and "scale_fix" not in settings:
        settings["scale_fix"] = "pad"

    # Меню для настройки параметров
    if not (skip_menu or args.skip_menu):
        menu = Menu(codec, settings)
        menu.show()
    else:
        print("Skipping menu, using settings from options.json")

    # Commander для генерации команд
    cmd_builder = commander.Commander(codec, settings)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not args.output_dir:
        output_dir = os.path.join(script_dir, "output")  # тут можно поменять папку выходных файлов
    else:
        output_dir = args.output_dir

    os.makedirs(output_dir, exist_ok=True)

    start_time = datetime.now()

    Menu.clear_screen()

    for file in files:
        if not os.path.exists(file):
            print(f"File not found: {file}")
            continue

        cmd = cmd_builder.build_ffmpeg_command(file, output_dir)
        print(f"Running:\n{cmd}\n")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while processing {file}: {e}")

    end_time = datetime.now()
    total_duration = end_time - start_time
    print(f"All done! Total processing time: {total_duration}")

    input("Press Enter to open the output folder, or close this window manually.")
    helpers.os_adapter.open_directory(output_dir)


if __name__ == "__main__":
    main()
