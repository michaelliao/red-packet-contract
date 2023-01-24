pragma circom 2.0.0;

include "./mimc.circom";

template Passcode() {
    signal input addr;
    signal input secret;
    signal output out;

    component hash = MiMC7(6);

    hash.x_in <== (addr + secret);
    hash.k <== 1234567;
    out <== hash.out;
}

component main {public [addr]} = Passcode();
