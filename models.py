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
