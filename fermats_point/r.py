#!/usr/bin/python3

import os
from sys import argv

option = argv[1]

match option:
    case "ll":
        os.system("manim main.py -p -r 854,480 --fps 5 --disable_caching")
    case "lfps":
        os.system(f"manim main.py -p -r 854,480 --fps {argv[2]} --disable_caching")
    case "l":
        os.system("manim main.py -pql --disable_caching")
    case "h":
        os.system("manim main.py -p -r 1280,720 --fps 60 --disable_caching")
    case "hh":
        os.system("manim main.py -pqh --disable_caching")
