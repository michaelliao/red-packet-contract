#!/usr/bin/env bash

echo 'generate powers of tau...'
rm -rf ptau
mkdir ptau
cd ptau

echo 'start a new ptau...'
snarkjs powersoftau new bn128 12 pot12_0000.ptau -v

echo 'generate random text...'
rnd1=""
rnd2=""
for i in {1..8}; do
    n=$(($RANDOM % 100))
    rnd1="$rnd1$n"
    n=$(($RANDOM % 100))
    rnd2="$rnd2$n"
done

echo 'contribute to the ceremony...'
snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau --name="First contribution" -v -e="$rnd1"

echo 'start phase 2...'
snarkjs powersoftau prepare phase2 pot12_0001.ptau ../passcode_js/pot12_final.ptau -v

echo 'generate .zkey file...'
snarkjs groth16 setup ../passcode.r1cs ../passcode_js/pot12_final.ptau ../passcode_js/passcode_0000.zkey

echo 'contribute to the phase 2 of the ceremony...'
snarkjs zkey contribute ../passcode_js/passcode_0000.zkey ../passcode_js/passcode_0001.zkey --name="1st Contributor Name" -v -e="$rnd2"

echo 'generate solidity code...'
snarkjs zkey export solidityverifier ../passcode_js/passcode_0001.zkey ../contracts/verifier.sol

echo 'export the verification key...'
snarkjs zkey export verificationkey ../passcode_js/passcode_0001.zkey ../passcode_js/verification_key.json
