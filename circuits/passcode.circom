pragma circom 2.0.0;

include "./mimc.circom";

template Passcode() {
    signal input addr;
    signal input secret;
    signal output out;

    component hash = MiMC7(3);

    hash.x_in <== (addr + secret);
    hash.k <== 123456789;
    out <== hash.out;
}

component main {public [addr]} = Passcode();
