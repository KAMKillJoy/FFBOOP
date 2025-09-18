import os


class Menu:
    def __init__(self, codec, settings):
        """
        codec    - объект Codec
        settings - словарь для хранения выбранных значений параметров
        """
        self.codec = codec
        self.settings = settings

    def show(self):
        while True:
            self.clear_screen()
            print("Select option:")

            options = list(self.codec.params.keys())
            for i, param in enumerate(options, 1):
                val = self.settings.get(param, "not set")
                print(f"{i}. {param} (Now: {val})")

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
                self.handle_fix_resolution()
                continue

            if choice_idx < 0 or choice_idx >= len(options):
                continue

            param = options[choice_idx]
            if param == "scale":
                self.handle_scale()
            elif param == "crf":
                self.handle_crf()
            elif param == "audio bitrate":
                self.handle_audio_bitrate()
            elif param == "fps":
                self.handle_fps()
            else:
                self.handle_param(param)

    def handle_param(self, param):
        self.clear_screen()
        allowed = self.codec.params[param]
        if allowed is None:
            # свободный ввод
            val = input(f"Enter value for {param} (empty to go back): ").strip()
            if val == "":
                return
            self.settings[param] = val
        else:
            # список вариантов
            while True:
                self.clear_screen()
                print(f"Choose {param} (empty to go back):")
                for i, v in enumerate(allowed, 1):
                    print(f"{i}. {v}")
                choice = input("> ").strip()
                if choice == "":
                    return
                try:
                    idx = int(choice) - 1
                    self.settings[param] = allowed[idx]
                    return
                except (ValueError, IndexError):
                    print("Invalid choice, try again.")

    def handle_scale(self):
        while True:
            self.clear_screen()
            print("Scale options (empty to go back):")
            print("1. Height")
            print("2. Width")
            print("3. Resolution (WxH)")
            print("r. Reset to original")
            choice = input("> ").strip()
            if choice == "":
                break
            elif choice == "1":
                self.clear_screen()
                val = input("Enter height value (Width adjusts automatically): ").strip()
                if val != "":
                    self.settings["scale"] = f"-1:{val}"
                    break
            elif choice == "2":
                self.clear_screen()
                val = input("Enter width value (Height adjusts automatically): ").strip()
                if val != "":
                    self.settings["scale"] = f"{val}:-1"
                    break
            elif choice == "3":
                self.clear_screen()
                val = input("Enter resolution (WxH): ").strip()
                if val != "":
                    self.settings["scale"] = val
                    break
            elif choice.lower() == "r":
                self.settings["scale"] = None
                break
            else:
                print("Invalid choice, try again.")

    def handle_fix_resolution(self):
        while True:
            self.clear_screen()
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

    def handle_crf(self):
        min_crf, max_crf = self.codec.params["crf"]
        while True:
            self.clear_screen()
            val = input(
                f'Input CRF in range {min_crf} - {max_crf} (empty to go back):').strip()
            if val == "":
                break
            try:
                val_int = int(val)
                if min_crf <= val_int <= max_crf:
                    self.settings["crf"] = val_int
                    break
            except ValueError:
                print("Invalid input, must be a number")

    def handle_audio_bitrate(self):
        min_ab, max_ab = self.codec.params["audio bitrate"]
        while True:
            self.clear_screen()
            val = input(
                f'Enter audio bitrate (kbps, numbers only, {min_ab}-{max_ab}) (empty to go back):').strip()
            if val == "":
                break
            try:
                val_int = int(val)
                if min_ab <= val_int <= max_ab:
                    self.settings["audio bitrate"] = val_int
                    break
            except ValueError:
                print("Invalid input, must be a number")

    def handle_fps(self):
        self.clear_screen()
        while True:
            val = input(
                'Input FPS (empty to go back, "r" to reset):').strip()
            if val == "":
                break
            elif val.lower() == "r":
                self.settings["fps"] = "don't change"
                break
            try:
                val_int = int(val)
                self.settings["fps"] = val_int
                self.clear_screen()
                break
            except ValueError:
                self.clear_screen()
                print("Invalid input, must be a number or 'r'")
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
