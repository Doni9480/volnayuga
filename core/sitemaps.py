from django.contrib.sitemaps import Sitemap

from hotel.models import Hotel


class HotelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Hotel.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

    def location(self, obj):
        return '/%s/%s' % (obj.region.slug, obj.id)