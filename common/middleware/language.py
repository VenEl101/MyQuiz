from django.utils import translation

class LanguageFromHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.headers.get("Accept-Language", "uz")[:2]
        if lang not in ["uz", "ru", "en"]:
            lang = 'uz'
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        translation.deactivate()
        return response
