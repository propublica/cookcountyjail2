
import jailscraper.spiders.inmate_spider as inmate_spider
from tests import TEST_INMATES_CSV


EXPECTED = [
    'http://www2.cookcountysheriff.org/search2/details.asp?jailnumber=2015-0904292',  # NOQA: E501
    'http://www2.cookcountysheriff.org/search2/details.asp?jailnumber=2017-0608010',  # NOQA: E501
    'http://www2.cookcountysheriff.org/search2/details.asp?jailnumber=2017-0612061',  # NOQA: E501
]


def test_generate_seeded_urls():
    spider = inmate_spider.InmatesSpider()
    urls = spider._generate_seeded_urls(TEST_INMATES_CSV)
    assert EXPECTED == urls
