# Requirements:
#   opencc

import opencc
import argparse

PHRASES = {
    "怪物猎人": "魔物猎人",
    "怪异炼化": "傀異鍊成",
}

PHRASES_T = {
    "遠端": "遠程",
    "煉化": "鍊成",
    "移動裝置": "行動裝置",
    "單擊": "點擊",
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help="Input file")
    parser.add_argument('output', type=str, help="Output file")
    args = parser.parse_args()

    with open(args.input) as f:
        content = f.read()
    
    converter = opencc.OpenCC('s2twp.json')
    p = content.replace('“', '「').replace('”', '」')
    while True:
        ended = True
        for k, v in PHRASES.items():
            if k in p:
                p = p.replace(k, v)
                ended = False
        if ended:
            break
    pp = converter.convert(p)
    while True:
        ended = True
        for k, v in PHRASES_T.items():
            if k in pp:
                pp = pp.replace(k, v)
                ended = False
        if ended:
            break
    
    with open(args.output, "w") as f:
        f.write(pp) 


if __name__ == '__main__':
    main()
