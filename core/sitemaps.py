from django.contrib.sitemaps import Sitemap

from hotel.models import Hotel
from region.models import Region


class HotelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Hotel.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

    def location(self, obj):
        return '/%s/%s' % (obj.city.slug, obj.id)


class RegionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Region.objects.all()

    def location(self, obj):
        return '/%s' % (obj.slug)