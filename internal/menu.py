from internal import helpers
from internal.helpers import os_adapter


class Menu:
    def __init__(self, codec, settings):
        """
        codec    - объект Codec
        settings - словарь для хранения выбранных значений параметров
        """
        self.codec = codec
        self.settings = settings

    @staticmethod
    def choose_codec_menu(codecs: list):
        print("Select codec:")
        for i, c in enumerate(codecs, 1):
            print(f"{i}. {c.name}")
        while True:
            choice = input("> ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(codecs):
                    return codecs[idx]
            except ValueError:
                pass
            print("Invalid choice, try again.")

    def show(self):
        while True:
            Menu.clear_screen()
            print("Select option:")

            options = list(self.codec.params.keys())
            for i, param in enumerate(options, 1):
                val = self.settings.get(param, "not set")
                print(f"{i}. {self.codec.params[param].get('label')} (Now: {val})")

            # Проверяем Fix resolution
            extra_idx = len(options) + 1
            if self.codec.even_res:
                fix_val = self.settings.get("scale_fix")
                print(f"{extra_idx}. Fix resolution (Now: {fix_val})")

            print("Enter empty input to finish selection")
            choice = input("> ").strip()
            if choice == "":
                break

            try:
                choice_idx = int(choice) - 1
            except ValueError:
                continue

            # Подменю Fix resolution
            if self.codec.even_res and choice_idx == len(options):
                self.__handle_fix_resolution()
                continue

            if choice_idx < 0 or choice_idx >= len(options):
                continue

            param = options[choice_idx]
            if param == "scale":
                self.__handle_scale()
            else:
                self.__handle_param(param)

    def __handle_param(self, param: str):
        Menu.clear_screen()
        param_dict = self.codec.params[param]
        param_type = param_dict["type"]
        if param_type == "direct":
            # свободный ввод
            allowed = param_dict.get("allowed")
            print(allowed)

            if param_dict.get("resettable"):
                help_string = param_dict["help"] + helpers.RESETTABLE_HELP_STRING
            else:
                help_string = param_dict["help"]

            while True:
                val = input(help_string.strip())

                if val == "":
                    return
                if param_dict["resettable"] and (val == "r" or val == "reset"):
                    self.settings[param] = helpers.DONT_CHANGE_STRING
                    return
                if allowed and val in allowed:
                    self.settings[param] = val
                    return
                if not allowed:
                    self.settings[param] = val
                    return

        elif param_type == "choice":
            # список вариантов
            while True:
                choices = param_dict["choices"]
                Menu.clear_screen()
                print(param_dict.get("help", ""))
                for i, v in enumerate(choices, 1):
                    print(f"{i}. {choices[i - 1]['label']}")
                choice = input("> ").strip()
                if choice == "":
                    return
                try:
                    idx = int(choice) - 1
                    self.settings[param] = param_dict["choices"][idx]["command_value"]
                    return
                except (ValueError, IndexError):
                    print("Invalid choice, try again.")

    def __handle_scale(self):
        Menu.clear_screen()
        while True:
            print("Scale options (empty to go back):")
            print("1. Height")
            print("2. Width")
            print("3. Resolution (WxH)")
            print("r. Reset to original")
            choice = input("> ").strip()
            if choice == "":
                Menu.clear_screen()
                break
            elif choice == "1":
                Menu.clear_screen()
                val = input("Enter height value (Width adjusts automatically): ").strip()
                if val != "":
                    self.settings["scale"] = f"-1:{val}"
                    Menu.clear_screen()
                    break
                Menu.clear_screen()
            elif choice == "2":
                Menu.clear_screen()
                val = input("Enter width value (Height adjusts automatically): ").strip()
                if val != "":
                    self.settings["scale"] = f"{val}:-1"
                    Menu.clear_screen()
                    break
                Menu.clear_screen()
            elif choice == "3":
                Menu.clear_screen()
                val = input("Enter resolution (W:H): ").strip()
                if val != "":
                    self.settings["scale"] = val
                    Menu.clear_screen()
                    break
                Menu.clear_screen()
            elif choice.lower() == "r":
                self.settings["scale"] = None
                Menu.clear_screen()
                break
            else:
                Menu.clear_screen()
                print("Invalid choice, try again.")

    def __handle_fix_resolution(self):
        while True:
            Menu.clear_screen()
            print("Fix resolution options:")
            print("1. Add 1px padding (pad)")
            print("2. Crop 1px (crop)")
            print("3. Cancel")
            choice = input("> ").strip()
            if choice == "1":
                self.settings["scale_fix"] = "pad"
                break
            elif choice == "2":
                self.settings["scale_fix"] = "crop"
                break
            elif choice == "3":
                self.settings.pop("scale_fix", None)
                break
            elif choice == "":
                break
            else:
                print("Invalid choice, try again.")

    @staticmethod
    def clear_screen():
        os_adapter.clear_screen()
