from django.conf.urls import url

from .views import SignView, PayNotifyView

urlpatterns = [
    url(r"^sign/$", SignView.as_view(), name="sign"),
    url(r"^notify/$", PayNotifyView.as_view(), name="notify"),
    url(r"^refund/$", RefundView.as_view(), name="refund"),
]
