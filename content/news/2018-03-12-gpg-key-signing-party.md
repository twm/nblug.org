Title: GPG Key Signing Party
Tags: general meeting
Event: 2018-02-13 7:30 pm to 9:00 pm
Speaker: E. Frank Ball
Location: O'Reilly Media
Author: Tom Most

It's time for another GPG key signing.  We had one in May 2003 &amp; August 2014.

The point of this is to create a web of trust.  By signing someone's
public key, you state that you have checked that the person that uses a
certain keypair, is who he says he is and really is in control of the
private key.  This way a complete network of people who trust each other
can be created.  This network is called the strongly connected set.
Information about it can be found at http://pgp.cs.uu.nl/

Before the meeting:

1. Generate a public/private keypair with the `gpg --gen-key`
command (accept the defaults), see `man gpg` for more info.

2. Upload your key to a keyserver:

        gpg --send-keys --keyserver keyserver.ubuntu.com

3. Print out the key fingerprint with `gpg --fingerprint`
Also include your full name, email address, and Key ID#.
Bring this to the meeting,
and optionally make extra copies to hand out.

4. Email me at frank@nblug.org with the fingerprint, email address, full
name, and Key ID.  I'll have a list of everyone's info to hand out.

During the meeting:

Verify your GPG key fingerprint on the list I hand out and
verify your identity (with photo ID).

After the meeting:

1. Download the all of the keys for the fingerprints verified at the meeting

2. Add them to your keyring

3. Sign them

4. Upload your key again.

More info:

https://help.ubuntu.com/community/GnuPrivacyGuardHowto

http://cryptnet.net/fdp/crypto/keysigning_party/en/keysigning_party.html
