from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register
class ThreeDHook(CMSApp):
    name = _("3Dhook")
    app_name = '3D'

    def get_urls(self, page=None, language=None, **kwargs):
        return ["3D.urls"]