import string
import rsa 
import base64
from urllib.parse import quote_plus, unquote

SIGN_TYPE = "SHA-256"


def order_data(payload):
    lst = []
    for key, value in payload.items():
        lst.append("{}={}".format(key, value))
    lst.sort()
    order_payload = "&".join(lst)
    return order_payload


def remove_order_data(payload):
    lst = []
    for key, value in payload.items():
        if key == 'sign' or key == 'sign_type':
            pass
        else:
            lst.append("{}={}".format(key, value))
    lst.sort()
    order_payload = "&".join(lst)
    return order_payload


def sign(payload, private_key=None):
    private_key = rsa.PrivateKey._load_pkcs1_pem(private_key)
    sign = rsa.sign(payload.encode('utf-8'), private_key, SIGN_TYPE)
    b64sing = base64.encodebytes(sign).decode("utf8").replace("\n", "")
    return b64sing


def urlencode_data(payload, sign):
    lst = []
    for key, value in payload.items():
        lst.append("{}={}".format(
            key, quote_plus(value, encoding='utf-8')))
    lst.sort()
    order_payload = "&".join(lst)
    if sign:
        order_payload += "&sign=%s" % quote_plus(sign, encoding='utf-8')
    return order_payload


def check_sign(payload, sign, public_key=None):
    sign = base64.b64decode(sign)
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    return rsa.verify(payload.encode('utf-8'), sign, pubkey)


def check_ali_sign(payload, sign, alipay_public_key=None):
    sign = base64.b64decode(sign)
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(alipay_public_key)
    res = False
    try:
        res = rsa.verify(payload.encode('utf-8'), sign, pubkey)
    except Exception as e:
        res = False
    return res
