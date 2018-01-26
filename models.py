from django.db import models

class Order(models.Model):
    subject = models.CharField(max_length=256, verbose_name='订单标题')
    out_trade_no = models.CharField(max_length=64, null=True, blank=True, verbose_name='商户网站唯一订单号')
    product_code = models.CharField(max_length=64, default='QUICK_MSECURITY_PAY', verbose_name='销售产品码')
    total_amount = models.FloatField(help_text='单位为元，精确到小数点后两位，取值范围[0.01,100000000]', verbose_name='订单总金额')
    body = models.CharField(max_length=128, null=True, blank=True, verbose_name='订单描述')
    trade_no = models.CharField(max_length=64, null=True, blank=True, verbose_name='支付宝系统中的交易流水号')
    busname = models.CharField(max_length=16, null=True, blank=True, verbose_name="业务")
    time_end = models.DateTimeField(null=True, blank=True, verbose_name="支付完成时间")
    status = models.BooleanField(default=False, verbose_name='支付完成状态')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Refund(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    out_trade_no = models.CharField(max_length=64,  verbose_name="商户订单号")
    trade_no = models.CharField(
        max_length=64, null=True, blank=True, verbose_name='支付宝系统中的交易流水号')
    out_refund_no = models.CharField(
        max_length=64, null=True, blank=True, verbose_name="商户退款单号")
    refund_amount = models.FloatField(
        verbose_name="退款金额", help_text="订单总金额，单位元")
    refund_reason = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='退款原因')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, default="0", verbose_name="状态", choices=(
        ("1", "完成"), ("0", "未完成")))

    def __str__(self):
        return self.out_trade_no
