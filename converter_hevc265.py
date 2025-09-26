#!/usr/bin/env python3

from converter import main
from internal.my_codecs import hevc265

if __name__ == "__main__":
    main(preselected_codec=hevc265, skip_menu=False)
