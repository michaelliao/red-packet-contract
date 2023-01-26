#!/usr/bin/env python3
#
# Requirement: PyYAML
#
# pip3 install pyyaml
#

import os, re, yaml
import json 


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_dir = os.path.join(base_dir, 'static', 'icons')

    icon_files = list_icons(icon_dir)
    # remove default:
    del icon_files['default']
    for k, v in icon_files.items():
        print(f'found token: {k} => {v}')

    with open(os.path.join(base_dir, 'tokens.yml'), 'r') as fp:
        chains = yaml.load(fp, Loader=yaml.BaseLoader)

    icons = {}
    for chainName, chainInfo in chains.items():
        chainId = chainInfo['chain']
        addrs = {}
        icons[chainId] = addrs
        print(f'found chain: {chainName} => {chainId}')
        tokens = merge_tokens(chainInfo['tokens'])
        for token, address in tokens.items():
            if re.match(r'^0x[0-9a-fA-F]{40}$', address):
                if token in icon_files:
                    addrs[address.lower()] = icon_files[token]
                else:
                    print(f'WARN: token {token} has no icon.');
            else:
                print(f'ERROR: invalid address {address} for token {token}')

    js = '// auto-generated\nwindow.ICONS = '+ json.dumps(icons, indent=2)
    print(js)

    with open(os.path.join(base_dir, 'static', 'js', 'icons.js'), 'w') as f:
        f.write(js)


def merge_tokens(ts):
    d = {}
    for t in ts:
        for k, v in t.items():
            d[k] = v
    return d


def list_icons(d):
    fs = os.listdir(d)
    icons = {}
    for f in fs:
        m = re.match(r'^(\w+)\.svg$', f)
        if m:
            icons[m.group(1)] = f'/static/icons/{f}'
    return icons

#     icons = {}
#     for chain in os.listdir(icon_dir):
#         chainId = getChainId(chain)
#         if chainId > 0:
#             addrs = {}
#             icons[str(chainId)] = addrs
#             chain_dir = os.path.join(icon_dir, chain)
#             for token in os.listdir(chain_dir):
#                 m = re.match(r'^(0x[0-9a-fA-F]{40})\.svg$', token)
#                 if m:
#                     addr = m.group(1)
#                     if token.lower() != token:
#                         print(f'NOTE: rename {token} to {token.lower()}...')
#                         os.rename(os.path.join(chain_dir, token), os.path.join(chain_dir, token.lower()))
#                     addrs[addr.lower()] = f'icons/{chain}/{token.lower()}'
#                 else:
#                     print(f'WARN: invalid file: {icon_dir}/{chain}/{token}')
#         else:
#             print(f'WARN: invalid chain: {chain}')


# def getChainId(s):
#     m = re.match(r'^([0-9]+).*$', s)
#     if m:
#         return int(m.group(1))
#     return 0


if __name__ == '__main__':
    main()
