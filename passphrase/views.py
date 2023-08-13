from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from passphrase.passphrase_validation import (count_valid_passphrases_advanced,
                                              count_valid_passphrases_basic)


@csrf_exempt
@require_http_methods(["POST"])
def basic_passphrase_validation_view(request):
    passphrases_text = request.body.decode("utf-8")
    passphrases = passphrases_text.split("\n")
    return HttpResponse(str(count_valid_passphrases_basic(passphrases)))


@csrf_exempt
@require_http_methods(["POST"])
def advanced_passphrase_validation_view(request):
    passphrases_text = request.body.decode("utf-8")
    passphrases = passphrases_text.split("\n")
    return HttpResponse(str(count_valid_passphrases_advanced(passphrases)))
