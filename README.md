# python-alipay
Use Python3, Django, Django-rest-framework to achieve alipay payment.

签名、服务器异步通知，退款操作

## 支付宝第三方支付流程

1. 注册企业账户： https://memberprod.alipay.com/account/reg/enterpriseIndex.htm按步骤填写，注册完成后可获取支付宝企业账户
2. 登录支付宝开放平台：https://open.alipay.com/platform/home.htm
3. 需要开通系统服务商ISV/自研开发者这两个合作伙伴角色，用户PID需要保存 https://open.alipay.com/platform/accountSetting.htm
4. 创建应用：https://openhome.alipay.com/platform/appManage.htm 需要开通APP支付，然后进行签约，支付宝后台审核通过即可（其他功能安需求添加即可）
5. 设置接口加签方式：采用RSA2方式在该地址：https://docs.open.alipay.com/291/106097下载mac版的密钥生成器
6. 生成密钥（私钥和公钥，私钥要求自己保存，公钥上传到支付宝。自己的公钥上传后，支付宝会生成一个支付宝公钥）
一个app应该有三个密钥：一个自己生成的私钥，一个自己生成的公钥，一个支付宝生成的公钥（我们后台会用到支付宝公钥，自己的私钥，私钥要保留好，如果私钥丢失，需要重新配置）
7. 提交审核，等待通过

开发需要：1.app_id、2.用户私钥、3.支付宝公钥

## App支付请求参数说明(必传字段)

    appid（应用id）
    method (接口名称，若是APP支付接口值是：alipay.trade.app.pay)
    format (json)
    charset (UTF-8)
    sign_type (签名算法类型RSA2和RSA，推荐使用RSA)
    sign (签名)
    timestamp (请求时间 格式是：2014-07-24 03:07:50)
    version （版本号：1.0）
    notify_url （支付宝服务器主动通知商户服务器里指定的页面）
    biz_content （业务请求参数）
    
    业务参数必传字段
    
    subject(商品标题)
    out_trade_no（商户网站唯一订单号）
    total_amount （价钱，字符串类型，单位是元）
    product_code （销售商品码： APP支付的固定值：QUICK_MSECURITY_PAY）

### 示例代码：
```
biz_content = {
    'subject': subject,
    'total_amount': '%.2f' % float(total_amount),
    'product_code': 'QUICK_MSECURITY_PAY',
    'out_trade_no': out_trade_no,
}

payload = {
    'app_id': app_id,
    'method': 'alipay.trade.app.pay',
    'charset': 'UTF-8',
    'format': 'json',
    'sign_type': 'RSA2',
    'timestamp': timestamp,
    'version': '1.0',
    'notify_url': notify_url,
    # 关于biz_content一定要对biz_content进行json.dumps操作，进行urlencode、生成sign时，会把biz_content整体当成一个value，所以要求该值是一个严格的json.
    'biz_content': json.dumps(biz_content, separators=(',', ':')), # separators=(',', ':')可以用来去掉json中的空格来压缩json
}
```
    
## 请求示例的获取

### 请求参数按照key=value&key=value方式拼接的未签名原始字符串：

```
app_id=2015052600090779&biz_content={"timeout_express":"30m","product_code":"QUICK_MSECURITY_PAY","total_amount":"0.01","subject":"1","body":"我是测试数据","out_trade_no":"IQJZSRC1YMQB5HU"}&charset=utf-8&format=json&method=alipay.trade.app.pay&notify_url=http://domain.merchant.com/payment_notify&sign_type=RSA2&timestamp=2016-08-25 20:26:31&version=1.0
```

### 对原始字符串进行签名:

1. 筛选并排序
    
        获取所有请求参数，不包括字节类型参数，如文件、字节流，剔除sign字段，剔除值为空的参数，并按照第一个字符的键值ASCII码递增排序（字母升序排序），如果遇到相同字符则按照第二个字符的键值ASCII码递增排序，以此类推



2. 拼接
        
        将排序后的参数与其对应值，组合成“参数=参数值”的格式，并且把这些参数用&字符连接起来，此时生成的字符串为待签名字符串

```
# 对payload数据进行排序和拼接
def order_data(payload):
    lst = []
    for key, value in payload.items():
        lst.append("{}={}".format(key, value))
    lst.sort()
    order_payload = "&".join(lst)
    return order_payload
```

3. 调用签名函数
    
        使用各自语言对应的SHA256WithRSA(对应sign_type为RSA2)或SHA1WithRSA(对应sign_type为RSA)签名函数利用商户私钥对待签名字符串进行签名，并进行Base64编码
```
import rsa
import base64

def sign(payload, private_key=None):
    private_key = rsa.PrivateKey._load_pkcs1_pem(private_key)
    sign = rsa.sign(payload.encode('utf-8'), private_key, SIGN_TYPE)
    b64sing = base64.encodebytes(sign).decode("utf8").replace("\n", "")
    return b64sing
```

### 把生成的签名赋值给sign参数，拼接到请求参数中
        
        最后对请求字符串的所有一级value（biz_content作为一个value）进行encode，编码格式按请求串中的charset为准，没传charset按UTF-8处理，获得最终的请求字符串

```
#  对所有value值进行urlencode操作
from urllib.parse import quote_plus

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
```
## 进行过urlencode的数据

```
app_id=2016081600254796&biz_content=%7B%22subject%22%3A%22%5Cu6d4b%5Cu8bd5%22%2C%22total_amount%22%3A%220.01%22%2C%22product_code%22%3A%22QUICK_MSECURITY_PAY%22%2C%22out_trade_no%22%3A%22alipay20171014%22%7D&charset=UTF-8&format=json&method=alipay.trade.app.pay&notify_url=http%3A%2F%2Fdongwu-inc.com%3A10014%2Falipay%2Fnotify%2F&sign_type=RSA2&timestamp=2017-10-14+14%3A03%3A50&version=1.0&sign=PbDyqQ%2BuAdJXWmEuJSFRq%2FiEPg7CJGbsf%2FexHOSG2%2FiW2TGigeFRKhZJNpxcImdkdcFLmFLlEhTNotfJKMDfhjFx0TJH0vVxQHECnkO5XpVpJ%2F2YZbj3fi8UPe2N%2FiZ9tJ5LBp%2Bj%2BXmBcW55lvsUA5s09bTgn5wU%2BhY4kiB6YO0U1CqARyPd6b2Nhs2A6jN4utyjzoUOvDQwXksmDB48qJSnJfdcfbxP1AtZ4nAVY2vtWZHPtQbj5NqY6jsNd2WxCRVqwHYdMZf0lHPwXa7ygVeALtIDhw%2FYXepOmTNJkYJs4sIpB8p9rpSgoY5A46SDThM90Vg5Q4c0d4kxWnG9%2FA%3D%3D

```

## 注意

1. 需对biz_content进行json.dumps操作将其转化为严格的json格式，生成sign和urlencode时都需要该操作；
2. 向前端传值时，需对整个数据的value（拼接字符串的value值）进行urlencode，其中包括sign的值；
3. 因对value进行urlencode, 所以需要biz_content为严格的json格式，单引号和双引号的urlencode不同，导致签名失败的原因大都是该位置出现了问题。
