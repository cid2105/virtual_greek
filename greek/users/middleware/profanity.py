from django.conf import settings
class ProfanityFilterMiddleware(object):
    def process_request(self, request):
		setattr(request, '_dont_enforce_csrf_checks', True)
        rpd = request.raw_post_data.lower()
        for w in settings.PROFANITIES_LIST:
            if rpd.find(w)!=-1:
                return HttpResponseRedirect("")