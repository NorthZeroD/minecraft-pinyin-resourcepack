# gen_lang_flypy.py

import json

LANG = {
    "language.code": "zho-Hans_szm",
    "language.name": "汉语拼音",
    "language.region": "首字母",
}

def load_mc_dict(path: str) -> dict[str, str]:
    mapping = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, val = line.split("\t")
            mapping[key] = val
    return mapping

def load_special_word_szm(path: str) -> dict[str, str]:
    mapping = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, val = line.split("\t")
            mapping[key] = val
    return mapping

def load_pass_key(path: str) -> set[str]:
    set = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            set.append(line)
    return set

def main(PATHS: dict[str, str]) -> None:
    mc_dict = load_mc_dict(PATHS["mc_dict"])
    special_word_szm = load_special_word_szm(PATHS["special_word_quanpin"])
    pass_key = load_pass_key(PATHS["pass_key"])

    special_keys = sorted(special_word_szm.keys(), key = len, reverse = True)

    with open(PATHS["language_file"], "r", encoding = "utf-8") as f:
        lang_data = json.load(f)

    result_data = {}
    missing = set()

    for k, v in lang_data.items():
        if k.startswith("item.minecraft.") or k.startswith("block.minecraft."):
            v_ = v

            if any(e in k for e in pass_key):
                result_data[k] = v
                continue

            for sw in special_keys:
                if sw in v:
                    v = v.replace(sw, special_word_szm[sw])

            result = ""
            for ch in v:
                if "\u4e00" <= ch <= "\u9fff":
                    t = mc_dict.get(ch, "#")
                    if t != "#":
                        result += t[0]
                    else:
                        result += "#"
                        missing.add(ch)
                else:
                    result += ch
            result_data[k] = f"{v_} | {result}"
        elif LANG.get(k):
            result_data[k] = LANG[k]
        else:
            result_data[k] = v

    with open(PATHS['output_file'], "w", encoding = "utf-8") as f:
        json.dump(result_data, f, ensure_ascii = False, indent = 2)

    print(f"完成生成: {PATHS['output_file']}, 字库缺少汉字数量: {len(missing)}")
    if missing:
        print("缺少的汉字: ", "".join(sorted(missing)))

if __name__ == "__main__":
    from main import PATHS
    main(PATHS)
