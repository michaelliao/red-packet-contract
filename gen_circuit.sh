#!/usr/bin/env bash

echo 'clean...'
rm -rf ./passcode.*
rm -rf ./passcode_js
rm -rf ./passcode_cpp

echo 'compile...'
circom circuits/passcode.circom --r1cs --wasm --sym

snarkjs info -r passcode.r1cs
snarkjs r1cs print passcode.r1cs passcode.sym
