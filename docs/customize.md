# Customize the Red Packet

The creator can customize the red packet by specifiying the URL parameters.

Switch account to the creator address and you can see the "Customize Your Red Packet" link on bottom of the red packet.

### How to Customize the Red Packet

In preview mode you can add parameters to URL and preview. Here are supported parameters:

- rpGreeting: the greeting words, default to "Best Wishes!";
- rpCreator: the creator name, default to the address of the creator;
- rpDisplayOpenInfo: show or hide the red packet status, default to "true";
- rpCoverImage: cover image of the red packet, default to "";
- rpOpenImage: image of open button, default to "";
- rpIconImage: image of the token, default to the token icon.

Example:

```
https://redpacket.eth.itranswarp.com/rp.html
?chain=1
&id=2
&rpGreeting=Hello%20World
&rpCreator=Crypto%20Michael
&rpDisplayOpenInfo=false
&rpCoverImage=https://example.com/path/to/bg.png
&rpOpenImage=/static/img/open.png
&rpIconImage=https://example.com/path/to/icon.svg
&preview=true
```

You have to sign the URL parameters to generate a valid URL after preview.

The generated URL can be copied and open in new tab of browser.

### Algorithm

A valid URL with signature contains `sig` for signature. To verify the signature, create a payload as follows:

```
let params = [];
params.push('chain=1'); // add chain parameter
params.push('id=2'); // add id parameter
params.push('rpGreeting=Hello World'); // add rpGreeting parameter, with ORIGINAL value (NOT the URL encoded)
params.push('rpCoverImage=https://example.com/path/to/bg.png'); // add rpCoverImage parameter, with ORIGINAL value (NOT the URL encoded)
// add more 'rpXxx' parameters
params.sort(); // sort the k-v
let message = params.join('&'); // build query string like 'chain=1&id=2&rpXxx=xxx&...'
// now call MetaMask for signature:
let sig = await getWeb3Provider().getSigner().signMessage(msg); // 0xda261a6f...
// append the sig to URL and remove the preview=true:
let url = 'https://redpacket.eth.itranswarp.com/rp.html?chain=1&id=2&rpXxx=xxx&sig='+sig;
```

This is make sure that only the creator of the red packet can customize it.
