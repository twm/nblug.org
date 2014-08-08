Title: Lightning Talks / Hackfest / GPG Key Signing
Tags: general meeting
Event: 2014-08-12 7:30 pm to 9:00 pm
Speaker: Frank Ball et al.
Location: O'Reilly Media
Author: Glenn Kerbein
Drupal_Node: 203

<span style="text-decoration: underline">Coordinator</span>: Frank Ball

## Lightning Talks:

Have something you would like to present, but don't have enough material for a full talk?  Here's your chance.  Talk about anything Linux related.

## Hackfest:

Bring your hardware to get help with it or just to show it off.


## GPG Key Signing Party:  

The point of this is to create a web of trust.  By signing someone's public key, you state that you have checked that the person that uses a certain keypair, is who he says he is and really is in control of the private key.  This way a complete network of people who trust each other can be created. This network is called the Strongly connected set. Information about it can be found at [http://pgp.cs.uu.nl/](http://pgp.cs.uu.nl/)

## Before the meeting:  
Create a GPG keypair, upload your public key to a keyserver, print out the fingerprint, mail it to me (frank@nblug.org) and bring copies to the meeting.

## Details:
1. Generate a public/private keypair with the <code>gpg --gen-key</code> command (accept the defaults), see <code>man gpg</code> for more info.
2. Upload your key to a keyserver:
<code>gpg --send-keys --keyserver keyserver.ubuntu.com <Key ID></code>
3. Print out the key "fingerprint" with 
<code>gpg --fingerprint <ID or eMail address></code>
Also include your full name, email address, and Key ID#.
Bring this to the meeting, and optionally make extra copies to hand out.
4. Email me at frank@nblug.org with the fingerprint, email, full name,
and Key ID.  I'll have a list of everyone's info to hand out.


## During the meeting:
Verify your GPG key fingerprint on the list I hand out and verify your identity (with photo ID).

## After the meeting:
Download the keys for the fingerprints verified at the meeting, add them to your keyring, sign them, and upload your key again.

### More info:

- [https://help.ubuntu.com/community/GnuPrivacyGuardHowto](https://help.ubuntu.com/community/GnuPrivacyGuardHowto)
- [http://cryptnet.net/fdp/crypto/keysigning_party/en/keysigning_party.html](http://cryptnet.net/fdp/crypto/keysigning_party/en/keysigning_party.html)

