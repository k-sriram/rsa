### Version 1.0
### RSA encryption and signing package
### Updated: 29/7/2011
### Sriram, Hariram, Sainath (IISER Pune)
"""
rsa is a Python package that can be used to for encryption and signing
of data.  It uses a non-standard flavour of the RSA algorithm developed
by the Authors.  It does public key based encryption. The takes input
and gives output in the str format. It supprots Key Genration,
Encrytion, Decryption, Signing and Verification.
"""

import rsa._keygen as keygen
import rsa._intmaths as intmaths
import rsa._strlist as strlist

def check_key_consistency(pk,sk):
    if pk[0]!=sk[0]:
        # if n of both keys is not same.
        raise KeyMismatch(1)
    elif intmaths.modpower(intmaths.modpower(2,pk[1],pk[0]),sk[1],sk[0])!=2:
        # if both keys don't represent the same key pair.
        raise KeyMismatch(2)

class KeyMismatch:
    """Exception raised when the two keys do not match."""
    def __init__(self,errno):
        self.errno=errno

    def __repr__(self):
        return "[Error No: %(errno)d] The given keys don't match." % {
                'errno':self.errno}


class KeyValue(list):
    """A Class to store the rsa Key."""
    def __init__(self,list_):
        if type(list_) == str:
            list.__init__(self, [int(i.strip('Ll')) for i in 
                                 list_.strip('[]()').split(',')])
        else:
            list.__init__(self, list_)

    def __getattr__(self,name):
        if name == 'n':
            return self[0]
        elif name in 'ed':
            return self[1]
        else:
            raise AttributeError(name)

    def __setattr__(self,name,value):
        if name == 'n':
            self[0] = value
        elif name in 'ed':
            self[1] = value
        else:
            list.__setattr__(self,name,value)


class Key:
    """
    This class stores the keys. It can encrypt, decrypt, sign and verify.
    Their are two types of keys: public key and secret key
    Public key is used to encrypt and verify.
    Secret Key is used to decrypt and sign.
    
    To send an encrypted message, do the following steps:
        1) Receiver generates a key pair.
        2) Receiver sends the public key to the sender.
        3) Sender encrypts the message using the public key.
        4) Sender sends the encrypted message.
        5) Receiver decrypts the message using the secret key.
        
    To send a signed message, do the following steps:
        1) Sender creates a key pair.
        2) Sender sends the public key through a *verified* channel.
        3) Sender signs using the private key.
        4) Sender sends the signed message.
        5) Receiver verifies using the public key.
    
    Use the following methods/attributes to do the above jobs.
        generate(keySize) to generate the key pair.
        encrypt(message) to get the encrypted cipher.
        decrypt(cipher) to get the original message.
        sign(message) to get the signed message.
        verify(message) to get the original message.
        pk and sk to access the public and secret key respectively.
        inflratio to get the inflation ratio i.e. the raio by which the
            message size will increase when encrypted or signed.  It is
            given by a tuple (a,b) representing a:b.
    """
    def __init__(self,pk=None,sk=None):
        """Pass the public and secret key if you know them."""
        self.setkeys(pk,sk)

    def __getattr__(self,name):
        if name == "pk":
            return self.get_publickey()
        elif name == "sk":
            return self.get_secretkey()
        elif name == "inflratio":
            return self.outSize,self.inSize
        else:
            raise AttributeError(name)
        return

    def __setattr__(self,name,value):
        if name == "pk":
            return self.set_publickey(value)
        elif name == "sk":
            return self.set_secretkey(value)
        else:
            self.__dict__[name] = value
        return

    def generate(self,keySize = 36):
        """
        Generates the key pair.
        keySize denotes the minimum guaranteed encpytion level.
        The program tries to encrypt at 2xkeySize. keySize should be >= 8.
        """
        # The key pair can be stored in three integers. n, e, d.
        # (n,e) forms the public key and (n,d) the secret key.
        self.e,self.d=None,None
        self.inSize=0
        while self.inSize==0:
            self.keySize=keySize
            n=0
            # Ensuring minimum encryption.
            while n<2**keySize:
                n, e, d=keygen.generate_key(2**keySize)
            self.set_publickey((n,e))
            self.set_secretkey((n,d))

    def encrypt(self, message):
        """
        Encrypts the given message.  Input and output should be strings.
        """
        # Encryption is done by first converting the input into blocks of size
        # inSize.  Then each block is converted into an integer.
        # These integers are encrypted using RSA.
        # They are again converted back to strings using outSize chars for one
        # string.
        # If key is not available return None.
        if self.e is None:
            return None
        cipherlist=[]
        # Making sure that the message can be stored in block of size inSize.
        # Done by adding extra '\0'
        trail=len(message)%self.inSize
        if trail!=0:
            trail=self.inSize-trail
            message=''.join([message]+['\0']*trail)
        # Conversion to integers.
        messagelist=strlist.str2list(message,self.inSize)
        # Encryption
        for i in messagelist:
            cipherlist.append(self._encryptel(i,self.e))
        # Conversion back to string. The number of '\0' added is put in the
        # front.
        cipher=chr(trail)+strlist.list2str(cipherlist,self.outSize)
        return cipher

    def decrypt(self,cipher):
        """
        Decrypts the given cipher.  Input and output should be strings.
        Returns garbage if the wrong secret code is used.
        """
        # See encrypt. Decryption uses the reverse process.
        # If key is not available return None.
        if self.d is None:
            return None
        # Conversion to integers
        cipherlist=strlist.str2list(cipher[1:],self.outSize)
        messagelist=[]
        # Decryption
        for i in cipherlist:
            messagelist.append(self._encryptel(i,self.d))
        # Conversion back to string.
        message=strlist.list2str(messagelist,self.inSize)
        # Removing the trailing '\0' added.
        if not cipher.startswith(chr(0)):
            message=message[:-ord(cipher[0])]
        return message

    def sign(self,message):
        """
        Encrypts the given message.  Input and output should be strings.
        """
        # Signing is implemented by encryption with secret key.
        # So keys are swapped and encryption is done.
        self.swapkeys()
        cipher=self.encrypt(message)
        self.swapkeys()
        return cipher
    def verify(self,cipher):
        """
        Verifies the given message.  Input and output should be strings.
        Returns garbage if unable to verify.
        """
        # Verification is implemented by decrypting with public key.
        # So keys are swapped and decryption is done.
        self.swapkeys()
        message=self.decrypt(cipher)
        self.swapkeys()
        return message

    def _calc_sizes(self,n):
        # Calculates the required sizes of blocks. See encrypt.
        self.outSize=(intmaths.rooflog(n,2)-1)/8+1
        self.inSize=(intmaths.rooflog(n+1,2)-1)/8

    def _encryptel(self,el,keyval):
        return intmaths.modpower(el,keyval[1],keyval[0])

    def set_publickey(self,pk):
        """Set the public key"""
        pk=KeyValue(pk)
        if self.d is not None:
            check_key_consistency(pk,self.d)
        self.e=pk
        self._calc_sizes(pk[0])
        
    def set_secretkey(self,sk):
        """Set the secret key"""
        sk=KeyValue(sk)
        if self.e is not None:
            check_key_consistency(self.e,sk)
        self.d=sk
        self._calc_sizes(sk[0])

    def setkeys(self,pk=None,sk=None):
        """Sets both the keys."""
        self.e,self.d=None,None
        if pk is not None:
            self.set_publickey(pk)
        if sk is not None:
            self.set_secretkey(sk)

    def get_publickey(self):
        """Get the public key"""
        return self.e
    def get_secretkey(self):
        """Get the secret key"""
        return self.d

    def swapkeys(self):
        """Swap the public and secret keys"""
        self.e,self.d = self.d,self.e
        return None

