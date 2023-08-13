from django.urls import path

from .views import (advanced_passphrase_validation_view,
                    basic_passphrase_validation_view)

urlpatterns = [
    path("basic/", basic_passphrase_validation_view, name="passphrase-basic"),
    path("advanced/", advanced_passphrase_validation_view, name="passphrase-advanced"),
]
