from helpers import ResolutionFixer


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
            fix_val = self.settings.get("scale_fix", "pad")  # pad по умолчанию
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
        else:
            self.handle_param(param)

def handle_fix_resolution(self):
    while True:
        print("Fix resolution options:")
        print("1. Add 1px padding (pad)")
        print("2. Crop 1px (crop)")
        print("3. Cancel")
        choice = input("> ").strip()
        if choice == "1":
            self.settings["scale_fix"] = ResolutionFixer.pad()
            break
        elif choice == "2":
            self.settings["scale_fix"] = ResolutionFixer.crop()
            break
        elif choice == "3":
            self.settings.pop("scale_fix", None)
            break
        elif choice == "":
            break
        else:
            print("Invalid choice, try again.")
