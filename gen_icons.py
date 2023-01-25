#!/usr/bin/env python3

import os, re
import sys
import json 


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_dir = os.path.join(base_dir, 'icons')
    icons = {}
    for chain in os.listdir(icon_dir):
        chainId = getChainId(chain)
        if chainId > 0:
            addrs = {}
            icons[chain] = addrs
            for token in os.listdir(os.path.join(icon_dir, chain)):
                m = re.match(r'^(0x[0-9a-f]{40})\.svg$', token)
                if m:
                    addr = m.group(1)
                    addrs[addr] = f'icons/{chainId}/{token}'
                else:
                    print(f'invalid file: {icon_dir}/{chain}/{token}')
        else:
            print(f'invalid chain: {chain}')
    js = 'window.ICONS = '+ json.dumps(icons, sort_keys=True, indent=2)
    print(js)
    with open('icons.js', 'w') as f:
        f.write(js)


def getChainId(s):
    try:
        return int(s)
    except ValueError as e:
        return 0


if __name__ == '__main__':
    main()
