# gen_mc_dict.py

import json

def load_hanzi_dict_formatted(path: str) -> dict[str, str]:
    mapping = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            hanzi, pinyin = line.split("\t")
            mapping[hanzi] = pinyin
    return mapping

def main(PATHS: dict[str, str]) -> None:
    dict = load_hanzi_dict_formatted(PATHS['hanzi_dict_formatted'])

    with open(PATHS['language_file'], "r", encoding="utf-8") as f:
        data = json.load(f)

    hanzi = set()
    for k, v in data.items():
        if k.startswith("item.minecraft.") or k.startswith("block.minecraft."):
            for ch in v:
                if "\u4e00" <= ch <= "\u9fff":
                    hanzi.add(ch)

    missing = 0
    with open(PATHS['mc_dict'], "w", encoding="utf-8") as f:
        for ch in sorted(hanzi):
            if ch in dict:
                f.write(f"{ch}\t{dict[ch]}\n")
            else:
                f.write(f"{ch}\t#\n")
                missing += 1

    print(f"处理完成，共输出 {len(hanzi)} 个汉字，其中 {missing} 个未找到拼音。")

if __name__ == "__main__":
    from main import PATHS
    main(PATHS)
