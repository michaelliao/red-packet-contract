#!/usr/bin/env bash

echo 'generate powers of tau...'

cd passcode_js

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
snarkjs powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau -v

echo 'generate .zkey file...'
snarkjs groth16 setup ../passcode.r1cs pot12_final.ptau passcode_0000.zkey

echo 'contribute to the phase 2 of the ceremony...'
snarkjs zkey contribute passcode_0000.zkey passcode_0001.zkey --name="1st Contributor Name" -v

echo 'generate solidity code...'
snarkjs zkey export verificationkey passcode_0001.zkey verification_key.json

snarkjs zkey export solidityverifier passcode_0001.zkey ../contracts/Verifier.sol
