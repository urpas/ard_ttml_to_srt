#!/usr/bin/env python3

import os
import sys
import xml.etree.ElementTree as ET
from collections import namedtuple

import pysubs2


PF = "{http://www.w3.org/ns/ttml}"

Sub = namedtuple("Sub", "text begin end")


def time_str_to_ms(time_str):
    h, m, s = [float(i) for i in time_str.split(":")]
    return pysubs2.make_time(h=h, m=m, s=s)


def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    subs = [] 
    for paragraph in root[1][0][1:]:
        sentence = ""
        begin = time_str_to_ms(paragraph.attrib["begin"])
        end = time_str_to_ms(paragraph.attrib["end"])
        for elem in paragraph:
            if elem.tag == f"{PF}span":
                sentence += elem.text
            elif elem.tag == f"{PF}br":
                sentence += "\n"
            else:
                raise ValueError(f"Unknown tag name: {elem.tag}")
        subs.append(Sub(sentence, begin, end))

    ssa_subs = pysubs2.SSAFile()

    for sub in subs:
        event = pysubs2.SSAEvent(start=sub.begin, end=sub.end, text=sub.text)
        ssa_subs.append(event)
        print(event)

    ssa_subs.save(sys.argv[1][:-5] + ".srt")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:\n\tard_ttml_to_srt.py: [file]")
    elif not os.path.exists(sys.argv[1]):
        print("The file does not exist. exiting.")
    else:
        main()
