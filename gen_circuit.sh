#!/usr/bin/env bash

echo 'clean...'
rm -rf ./passcode.*
rm -rf ./passcode_js
rm -rf ./passcode_cpp

echo 'compile...'
circom circuits/passcode.circom --r1cs --wasm --sym
