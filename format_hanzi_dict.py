# format_hanzi_dict.py

import re

tone_map = str.maketrans("āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ",
                         "aaaaeeeeiiiioooouuuuvvvv")

def remove_tone(pinyin: str) -> str:
    return pinyin.translate(tone_map)

def main(PATHS: dict[str, str]) -> None:
    with open(PATHS['hanzi_dict'], "r", encoding="utf-8") as f_in, \
         open(PATHS['hanzi_dict_formatted'], "w", encoding="utf-8") as f_out:
        for line in f_in:
            line = line.strip()
            if not line or "#" not in line:
                continue

            # 汉字就是行最后一个字符
            hanzi = line[-1]

            # 拼音在冒号和 # 之间
            pinyin = line.split(":")[1].split("#")[0].strip()
            pinyin = remove_tone(pinyin)

            f_out.write(f"{hanzi}\t{pinyin}\n")

if __name__ == "__main__":
    from main import PATHS
    main(PATHS)
