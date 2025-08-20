# gen_mc_dict_flypy.py

FIRST = [
    ('zh', 'v'),
    ('ch', 'i'),
    ('sh', 'u'),
    ('a', 'aa'),
    ('o', 'oo'),
    ('e', 'ee'),
]
FIRST.sort(key=lambda x: len(x[0]), reverse=True)

SECOND = [
    ('iang', 'l'),
    ('iong', 's'),
    ('uang', 'l'),

    ('ong', 's'),
    ('iao', 'n'),
    ('ian', 'm'),
    ('uan', 'r'),
    ('uai', 'k'),
    ('van', 'r'),
    ('ang', 'h'),
    ('eng', 'g'),
    ('ing', 'k'),
    
    ('ia', 'x'),
    ('ua', 'x'),
    ('an', 'j'),
    ('ao', 'c'),
    ('ai', 'd'),
    ('ie', 'p'),
    ('ue', 't'),
    ('en', 'f'),
    ('ei', 'w'),
    ('ui', 'v'),
    ('in', 'b'),
    ('ou', 'z'),
    ('uo', 'o'),
    ('iu', 'q'),
    ('un', 'y'),
    ('ve', 't'),
    ('vn', 'y'),

    ('a', 'a'),
    ('e', 'e'),
    ('i', 'i'),
    ('o', 'o'),
    ('u', 'u'),
    ('v', 'v')
]
SECOND.sort(key=lambda x: len(x[0]), reverse=True)

def pinyin_to_flypy(pinyin: str) -> str:
    first: str
    second: str

    for sm, code in FIRST:
        if pinyin.startswith(sm):
            first = code
            second = pinyin[len(sm):]
            break
    else:
        first = pinyin[0]
        second = pinyin[1:]

    if not second:
        return first

    for ym, code in SECOND:
        if second.startswith(ym):
            return first + code

    return pinyin



def main(PATHS: dict[str, str]) -> None:
    with open(PATHS['mc_dict'], "r", encoding="utf-8") as fin, \
         open(PATHS['mc_dict_flypy'], "w", encoding="utf-8") as fout:
        
        for line in fin:
            line = line.strip()
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) != 2:
                print(f"跳过异常行: {line!r}")
                continue

            hanzi, pinyin = parts
            flypy = pinyin_to_flypy(pinyin)
            fout.write(f"{hanzi}\t{flypy}\n")


if __name__ == "__main__":
    from main import PATHS
    main(PATHS)
