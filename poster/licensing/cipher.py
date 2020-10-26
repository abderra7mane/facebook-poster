#-*- coding: utf-8 -*-

from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto import Random


class CipherException(Exception):
    pass


class Cipher(object):
    """
    """
    class __impl(object):
        """
        """
        def __init__(self):
            self.publicKey = None
            self.privateKey = None

        def _importKey(self, key):
            try:
                return RSA.importKey(key)
            except Exception as e:
                raise CipherException(e.message)

        def importPublicKey(self, key):
            self.publicKey = self._importKey(key)

        def importPrivateKey(self, key):
            self.privateKey = self._importKey(key)

        @staticmethod
        def encode(message):
            return b64encode(message)

        @staticmethod
        def decode(encoded):
            return b64decode(encoded)

        def encrypt(self, message):
            if self.publicKey is None and \
                    self.privateKey is None:
                raise CipherException("No encryption key")

            key = self.publicKey
            if key is None:
                key = self.privateKey

            try:
                b64msg = self.encode(message)
                encmsg = key.encrypt(b64msg, 32)
                cipher = self.encode(encmsg[0])
                return cipher
            except Exception as e:
                raise CipherException(e.message)

        def decrypt(self, cipher):
            if self.privateKey is None:
                raise CipherException("No private key")

            key = self.privateKey

            try:
                encmsg = self.decode(cipher)
                b64msg = key.decrypt(encmsg)
                message = self.decode(b64msg)
                return message
            except Exception as e:
                raise CipherException(e.message)

        def sign(self, message):
            if self.privateKey is None:
                raise CipherException("No private key")

            signer = PKCS1_v1_5.new(self.privateKey)
            digest = SHA256.new()
            digest.update(self.decode(message))
            signature = signer.sign(digest)
            return self.encode(signature)

        def verify(self, message, signature):
            if self.publicKey is None and \
                    self.privateKey is None:
                raise CipherException("No encryption key")

            key = self.publicKey
            if key is None:
                key = self.privateKey

            signer = PKCS1_v1_5.new(key)
            digest = SHA256.new()
            digest.update(self.decode(message))
            return signer.verify(digest, self.decode(signature))

        @staticmethod
        def random(length):
            return Random.new().read(length)

    __instance = None

    def __init__(self):
        super(Cipher, self).__init__()

        if Cipher.__instance is None:
            Cipher.__instance = Cipher.__impl()

        self.__dict__['_Cipher__instance'] = Cipher.__instance

    def __getattr__(self, attr):
        return getattr(Cipher.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(Cipher.__instance, attr, value)
