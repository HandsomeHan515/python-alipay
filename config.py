APP_ID = ''

# 支付宝服务器向商户服务器发送支付异步通知接口
NOTIFY_URL = 'http://example.com/alipay/notify/'

PAY_URL = 'https://openapi.alipay.com/gateway.do?timestamp=TIMESTAMP&method=alipay.trade.pay&app_id=APPID&sign_type=RSA2&sign=SIGN&version=1.0&biz_content=BIZ_CONTENT&charset=utf-8&notify_url=NOTIFY_URL&format=json'

# 商户私钥
RSA_PRIVATE = """
-----BEGIN RSA PRIVATE KEY-----
...
...
...
-----END RSA PRIVATE KEY-----
"""

# 商户公钥
RSA_PUBLIC = """
-----BEGIN PUBLIC KEY-----
...
...
...
-----END PUBLIC KEY-----
"""

#支付宝公钥
ALIPAY_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
...
...
...
-----END PUBLIC KEY-----

"""
