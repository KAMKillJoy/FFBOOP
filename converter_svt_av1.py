#!/usr/bin/env python3

from converter import main
from internal.my_codecs import svt_av1

if __name__ == "__main__":
    main(preselected_codec=svt_av1, skip_menu=False)
