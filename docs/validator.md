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

    function check(address redpacketContract, uint256 redpacketId, address operator) external view returns (bool) {
        return (
            redpacketContract == 0xFe6667986f58F2F7ed1e7C17Cee3951d8ABb717f &&
            redpacketId == 1234 && 
            authorizedAddresses[operator]);
    }
}
```
