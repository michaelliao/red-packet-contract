# Proof

JavaScript code to generate proof.

### Generate Passcode Hash for Creator

Passcode is a uint256 that is hashed by creator address (all lowercase) and string password (case-sensitive, UTF-8 encoding):

```
// TODO: import ethersjs, snarkjs...

function hashString(str) {
    let arr = new TextEncoder().encode(str);
    return ethers.utils.keccak256(arr);
}

async function prove(addrBN, secretBN) {
    return await snarkjs.groth16.fullProve(
        {
            addr: addrBN.toString(),
            secret: secretBN.toString()
        },
        "passcode_js/passcode.wasm", "passcode_js/passcode_0001.zkey"
    );
}

async function passcodeHash() {
    let
        creator = '0xA1B2...',
        password = 'Bitcoin',
        passcode = hashString(creator.toLowerCase() + password);
        passcodeBN = ethers.BigNumber.from(passcode);

    let { proof, publicSignals } = await prove(ethers.BigNumber.from(0), passcodeBN);

    // get out from public signals:
    let passcodeHashBN = ethers.BigNumber.from(publicSignals[0]);
    return passcodeHashBN;
}

let hash = await passcodeHash();

// TODO: write hash to contract when create a red packet
```

### Generate Proof for Receiver

Receiver knows creator address and string password:

```
async function generateProof() {
    let
        creator = '0xA1B2...',
        password = 'Bitcoin',
        passcode = hashString(creator.toLowerCase() + password);
        passcodeBN = ethers.BigNumber.from(passcode);

    let
        account = '0x3C4D...', // receiver address
        accountBN = ethers.BigNumber.from(receiver),
        secretBN = passcodeBN.sub(accountBN); // passcode = address + secret

    // generate proof:
    let { proof, publicSignals } = await prove(accountBN, secretBN);
    let passcodeHashBN = ethers.BigNumber.from(publicSignals[0]);

    // check if out from public signals equals to passcodeHash read from contract:
    let passcodeHashBNFromContract = await readFromContract(...);
    if (!passcodeHashBN.eq(passcodeHashBNFromContract)) {
        alert('bad password!');
        return;
    }
    // prepare proof for contract call:
    let proofs = [
        proof.pi_a[0], proof.pi_a[1],
        // NOTE: the order of proof.pi_b is differ to pi_a and pi_c:
        proof.pi_b[0][1], proof.pi_b[0][0], proof.pi_b[1][1], proof.pi_b[1][0],
        proof.pi_c[0], proof.pi_c[1]
    ];
    // convert '12345678' to '0xbc614e':
    for (let i = 0; i < proofs.length; i++) {
        // string -> hex string:
        proofs[i] = ethers.BigNumber.from(proofs[i]).toHexString();
    }

    // Optional: call verifyProof() to validate the proof:
    let r = await contract.verifyProof(
            [proofs[0], proofs[1]], // a[2]
            [[proofs[2], proofs[3]], [proofs[4], proofs[5]]], // b[2][2]
            [proofs[6], proofs[7]], // c[2]
            [passcodeHashBN.toHexString(), accountBN.toHexString()] // i[2]
    );
    if (!r) {
        alert('bad proof');
        return;
    }

    // call contract open():
    let tx = await contract.open(redPacketId, proofs);
    await tx.wait(1);
}
```

PLEASE NOTE the order of `proof.pi_b` is differ to `pi_a` and `pi_c`.
