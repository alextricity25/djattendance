from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.deprecation import MiddlewareMixin

EXEMPT_URLS = [reverse('login'), reverse('logout'), reverse('home'), reverse('web_access:get-remote-address'),
               reverse('apimport:term_details'), reverse('apimport:process_csv'), reverse('apimport:save_data')]


class LoginRequiredMiddleware(MiddlewareMixin):  # http://onecreativeblog.com/post/59051248/django-login-required-middleware
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
      assert hasattr(request, 'user'), "The Login Required middleware\
          requires authentication middleware to be installed. Edit your\
          MIDDLEWARE_CLASSES setting to insert\
          'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
          work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
         'django.core.context_processors.auth'."

      if not request.user.is_authenticated():
        if request.path not in EXEMPT_URLS:
          return HttpResponseRedirect(reverse('login'))
