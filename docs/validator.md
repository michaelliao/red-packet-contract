# Validator

A validator address can be set when create a red packet.

Red packet contract will do check when open if validator address is not set to zero address:

```
function open(uint256 id, uint256[] memory proof) public returns (uint256) {
    RedPacketInfo storage p = redPackets[id];
    address condition = p.condition;
    if (condition != address(0)) {
        require(ICondition(condition).check(address(this), id, msg.sender), "Address rejected");
    }
    ...
}
```

Here is a simple validator contract:

```
contract Validator is ICondition {
    mapping(address => bool) internal authorizedAddresses;

    function check(address redRacketContract, uint256 redRacketId, address operator) external view returns (bool) {
        return (
            redRacketContract == 0xFe6667986f58F2F7ed1e7C17Cee3951d8ABb717f &&
            redRacketId == 1234 && 
            authorizedAddresses[operator]);
    }
}
```

Here are [examples of validators](https://github.com/michaelliao/red-packet-contract/blob/master/contracts/Validators.sol).

### Example of Use Validator

Steps for using a validator that require receiver holds a NFT-721:

1. Create red packet with validator address [0xE721E34C44583Ac42D8B1dFeCb2F2B8a34730e56](https://blockscan.com/address/0xE721E34C44583Ac42D8B1dFeCb2F2B8a34730e56);

2. Call validator method `setERC721(uint redPacketId, address nftAddr)`.

### Deployed Validators

Address-Pool Validator: [0xADD0051Cc477e65D5B4f13a1D055Aa3650dF7635](https://blockscan.com/address/0xADD0051Cc477e65D5B4f13a1D055Aa3650dF7635)

ERC20 Holder Validator: [0xE20EDb92d70fB1793446Ed497Bc2Bf5BCb2d6590](https://blockscan.com/address/0xE20EDb92d70fB1793446Ed497Bc2Bf5BCb2d6590)

NFT-721 Holder Validator: [0xE721E34C44583Ac42D8B1dFeCb2F2B8a34730e56](https://blockscan.com/address/0xE721E34C44583Ac42D8B1dFeCb2F2B8a34730e56)

NFT-1155 Holder Validator: [0xE1155A1004DA9F85A18ba97aB918c44467b35ef5](https://blockscan.com/address/0xE1155A1004DA9F85A18ba97aB918c44467b35ef5)

Time Based Validator: [0xAf000bA2B6612613006FDc2c252Da9C69ba5e64e](https://blockscan.com/address/0xAf000bA2B6612613006FDc2c252Da9C69ba5e64e)
