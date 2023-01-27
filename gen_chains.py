#!/usr/bin/env python3
#
# Requirement: PyYAML
#
# pip3 install pyyaml
#

import os, re, yaml, json 


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_dir = os.path.join(base_dir, 'static', 'icons')

    icon_files = list_icons(icon_dir)
    # remove default:
    del icon_files['default']
    for k, v in icon_files.items():
        print(f'found token: {k} => {v}')

    with open(os.path.join(base_dir, 'chains.yml'), 'r') as fp:
        chains = yaml.load(fp, Loader=yaml.BaseLoader)

    all = {}
    default_icon_file = '/static/icons/default.svg'

    for chainName, chainInfo in chains.items():
        chainId = chainInfo['chain']
        chain = {}
        chain['id'] = int(chainId)
        chain['name'] = chainName
        chain['scan'] = chainInfo['scan']
        chain['rpc'] = chainInfo['rpc']
        chain['testnet'] = chainName.lower().find('testnet') >= 0
        chain['native'] = '*ETH*'
        chain['tokens'] = []
        all[chainId] = chain
        print(f'found chain: {chainName} => {chainId}')
        # tokenName -> tokenAddress
        tokenAddrs = merge_tokens(chainInfo['tokens'])
        nativeToken = None
        for tokenName, tokenAddress in tokenAddrs.items():
            token = {
                'symbol': tokenName.upper(),
                'address': tokenAddress.lower()
            }
            chain['tokens'].append(token)
            # find icon file:
            if re.match(r'^0x[0-9a-fA-F]{40}$', tokenAddress):
                if tokenName in icon_files:
                    token['icon'] = icon_files[tokenName]
                else:
                    print(f'WARN: token {tokenName} has no icon.');
                    token['icon'] = default_icon_file
                if re.match(r'^0x[eE]{40}$', tokenAddress):
                    nativeToken = tokenName.upper()
            else:
                print(f'ERROR: invalid address {tokenAddress} for token {tokenName}')
        if nativeToken:
            chain['native'] = nativeToken
        else:
            print(f'ERROR: NO native token found for chain {chainName}')

    js = r'''// auto-generated
window.ETH_ADDRESS  = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee';
window.ZERO_ADDRESS = '0x0000000000000000000000000000000000000000';
'''
    js = js + 'window.BLOCKCHAINS = '+ json.dumps(all, indent=2)
    print(js)

    with open(os.path.join(base_dir, 'static', 'js', 'blockchains.js'), 'w') as f:
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
