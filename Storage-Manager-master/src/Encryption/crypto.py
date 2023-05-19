"""Code written by Jacquesne Jones unless otherwise specified."""

from passlib.handlers import argon2 as pw   # Use the newer argon2 algorithm with argon2-cffi package
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

# passlib docs: https://passlib.readthedocs.io/en/stable/contents.html
######################################################################


class Access:

    def __init__(self):
        self.access = []

    @staticmethod
    def generate_hash(pwd):
        return pw.argon2.hash(pwd)

    @staticmethod
    def verify_hash(pwd, hash_value):
        return pw.argon2.verify(pwd, hash_value)
