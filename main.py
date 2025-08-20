# main.py

import sys
import os
import shutil
from pathlib import Path

BUILD_PATH = './build/'
PATHS = {
    "language_file": "zh_cn.json",

    "hanzi_dict": "_hanzi_dict.txt",
    "pass_key": "_pass_key.txt",
    "special_word_quanpin": "_special_word_quanpin.txt",
    "special_word_szm": "_special_word_szm.txt",
    "special_word_flypy": "_special_word_flypy.txt",
    
    "hanzi_dict_formatted": f"{BUILD_PATH}hanzi_dict_formatted.txt",
    "mc_dict": f"{BUILD_PATH}mc_dict.txt",
    "mc_dict_flypy": f"{BUILD_PATH}mc_dict_flypy.txt",

    "output_file": f"{BUILD_PATH}zh_cn_output.json"
}

TYPES = [
    'clean',
    'quanpin',
    'szm',
    'flypy'
]

def check_files() -> int:
    flag: int = 0

    if not os.path.exists(PATHS['language_file']):
        print(f"必要文件 {PATHS['language_file']} 不存在")
        flag += 1
    if not os.path.exists(PATHS['hanzi_dict']):
        print(f"必要文件 {PATHS['hanzi_dict']} 不存在")
        flag += 1
    if not os.path.exists(PATHS['pass_key']):
        print(f"必要文件 {PATHS['pass_key']} 不存在")
        flag += 1
    if not os.path.exists(PATHS['special_word_quanpin']):
        print(f"必要文件 {PATHS['special_word_quanpin']} 不存在")
        flag += 1
    if not os.path.exists(PATHS['special_word_szm']):
        print(f"必要文件 {PATHS['special_word_szm']} 不存在")
        flag += 1
    if not os.path.exists(PATHS['special_word_flypy']):
        print(f"必要文件 {PATHS['special_word_flypy']} 不存在")
        flag += 1

    return flag

def clean_files() -> None:
    dir_path = Path(BUILD_PATH)
    if dir_path.exists() and dir_path.is_dir():
        try:
            shutil.rmtree(dir_path)
        except Exception:
            pass

def main(args = sys.argv[1:]) -> None:
    if len(args) < 1:
        print(f"用例: python3 main.py <{'|'.join(TYPES)}>")
        return
    
    type = args[0]
    
    if type not in TYPES:
        print(f"无效参数: {type}  可用参数列表: <{'|'.join(TYPES)}>")
        return
    
    if type == 'clean':
        clean_files()
        print("已清理 build 目录")
        return

    if check_files() > 0:
        print("任务出错: 必要文件不存在")
        return
    
    if not os.path.exists(BUILD_PATH):
        os.makedirs(BUILD_PATH)

    PATHS['output_file'] = f"{BUILD_PATH}{PATHS['language_file']}_{type}.json"

    from format_hanzi_dict import main as format_hanzi_dict
    format_hanzi_dict(PATHS)

    from gen_mc_dict import main as gen_mc_dict
    gen_mc_dict(PATHS)

    if type == 'quanpin':
        from gen_lang_quanpin import main as gen_lang_quanpin
        gen_lang_quanpin(PATHS)

    elif type == 'szm':
        from gen_lang_szm import main as gen_lang_szm
        gen_lang_szm(PATHS)

    elif type == 'flypy':
        from gen_mc_dict_flypy import main as gen_mc_dict_flypy
        gen_mc_dict_flypy(PATHS)
        from gen_lang_flypy import main as gen_lang_flypy
        gen_lang_flypy(PATHS)

if __name__ == "__main__":
    main(['clean'])
    main(['flypy'])
