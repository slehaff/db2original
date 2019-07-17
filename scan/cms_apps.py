from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register
class ScanHook(CMSApp):
    name = _("scanhook")
    app_name = 'scan'

    def get_urls(self, page=None, language=None, **kwargs):
        return ["scan.urls"]
