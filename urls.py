from django.conf.urls import url

from .views import SignView, PayNotifyView

urlpatterns = [
    url(r"^sign/$", SignView.as_view(), name="sign"),
    url(r"^notify/$", PayNotifyView.as_view(), name="notify"),
]
