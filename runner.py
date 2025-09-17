import os
import subprocess
import sys
from datetime import datetime

import commander
from helpers import load_defaults, create_defaults_json_if_missing, supported_codecs
from menu import Menu


def choose_codec():
    supported = supported_codecs()
    print("Select codec:")
    for i, c in enumerate(supported, 1):
        print(f"{i}. {c.name}")
    while True:
        choice = input("> ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(supported):
                return supported[idx]
        except ValueError:
            pass
        print("Invalid choice, try again.")


def main(preselected_codec=None):
    create_defaults_json_if_missing()

    files = sys.argv[1:]
    '''if not files:
        print("No input files. Drag & drop video files onto this script.")
        return'''

    # Выбор кодека
    if preselected_codec:
        codec = preselected_codec
    else:
        codec = choose_codec()

    # Загружаем стандартные значения
    settings = load_defaults(codec.name)

    # Меню для настройки параметров
    menu = Menu(codec, settings)
    menu.show()

    # Commander для генерации команд
    cmd_builder = commander.Commander(settings)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    start_time = datetime.now()

    for file in files:
        if not os.path.exists(file):
            print(f"File not found: {file}")
            continue

        cmd = cmd_builder.build_ffmpeg_command(file)
        print(f"Running:\n{cmd}\n")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while processing {file}: {e}")

    end_time = datetime.now()
    total_duration = end_time - start_time
    print(f"All done! Total processing time: {total_duration}")

    input("Press Enter to open the output folder, or close this window manually.")
    if os.name == "nt":
        os.startfile(output_dir)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.run([opener, output_dir])


if __name__ == "__main__":
    main()
