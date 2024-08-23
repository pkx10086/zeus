"""
# @Time    : 2020/8/24 15:26
# @Author  : tmackan
"""
from pyDes import des, PAD_PKCS5, ECB
import binascii


def id_encrypt(msg):
    """
    DES 加密，分组方式 ECB，填充方式 PAD_PKCS5
    :param msg: msg待加密字符串
    :return: 返回加密后字符串,16进制
    """
    secret_key = 'ccTo56DZ'
    iv = "ccTo56DZ"
    key = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    entry_msg = key.encrypt(msg, padmode=PAD_PKCS5)
    return binascii.b2a_hex(entry_msg).decode("utf8")


def id_decrypt(msg):
    """
    DES 解密，分组方式 ECB，填充方式 PAD_PKCS5
    :param msg: 16进制加密码
    :return: 解密字符串
    """
    secret_key = 'ccTo56DZ'
    iv = secret_key
    key = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    des_msg = key.decrypt(binascii.a2b_hex(msg), padmode=PAD_PKCS5)
    return des_msg.decode("utf8")


# a = id_decrypt("3D6D13FB0C0456F7")
# print(a)
# b = id_encrypt(a)
# print(b)
print(id_decrypt("1E982EC58C674EFD"))