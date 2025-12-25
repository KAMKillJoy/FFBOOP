#!/usr/bin/env python3

from converter import main
from internal.my_codecs import vp9

if __name__ == "__main__":
    main(preselected_codec=vp9, skip_menu=False)
