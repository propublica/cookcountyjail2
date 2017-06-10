"""
Scraper models
"""
import hashlib

from lxml import html
from datetime import datetime
from dateutil.relativedelta import relativedelta

class InmatePage(object):

    def __init__(self, content):
        self.tree = html.fromstring(content)

    def _strip(self, x):
        """Simple stripping for lists and strings."""
        if isinstance(x, list):
            x = ''.join(x)
        return x.strip().replace(u'\xa0', u' ')

    def _strip_lines(self, x):
        """Strip multiline fields."""
        filtered = []
        for row in x:
            row = row.strip()
            if not row.isspace():
                filtered.append(row)
        return '\n'.join(filtered)

    def _makedate(self, x):
        """Turns mm/dd/YYYY into YYYY-mm-dd"""
        x = self._strip(x)
        return datetime.strptime(x, '%m/%d/%Y').strftime('%Y-%m-%d')

    @property
    def age_at_booking(self):
        """Calculate age at booking."""
        birthdate_string = self._strip(self.tree.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[3]//text()'))
        birthdate = datetime.strptime(birthdate_string, '%m/%d/%Y')
        bookingdate = datetime.strptime(self.booking_date, '%Y-%m-%d')
        return relativedelta(bookingdate, birthdate).years

    @property
    def bail_amount(self):
        """Returns bail amount"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[2]/tr[2]/td[4]//text()')
        return self._strip(value)

    @property
    def booking_date(self):
        """Returns booking date"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[2]/tr[2]/td[1]//text()')
        return self._makedate(value)

    @property
    def booking_id(self):
        """Returns booking id (also known as jail number)"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[1]//text()')
        return self._strip(value)

    @property
    def charges(self):
        """Returns charges"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[2]/tr[4]/td[1]//text()')
        return self._strip_lines(value)

    @property
    def court_date(self):
        """Returns next court date"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[3]/tr[2]/td[1]//text()')
        return self._makedate(value)

    @property
    def court_location(self):
        """Returns next court date location"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[3]/tr[2]/td[2]//text()')
        return self._strip_lines(value)

    @property
    def gender(self):
        """Returns gender"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[5]//text()')
        return self._strip(value)

    @property
    def housing_location(self):
        """Returns housing location"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[2]/tr[2]/td[2]//text()')
        return self._strip(value)

    @property
    def height(self):
        """Returns height"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[6]//text()')
        return self._strip(value)

    @property
    def inmate_hash(self):
        """Return hash that should identify inmate approximately uniquely"""
        rawname = self.tree.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[2]//text()')
        name = self._strip(rawname).replace(' ', '')

        birthdate_raw = self.tree.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[3]//text()')
        birthdate = self._strip(birthdate_raw).replace('/', '')

        id = '{0}{1}{2}{3}'.format(name, birthdate, self.race, self.gender).encode('utf-8')
        return hashlib.sha256(id).hexdigest()

    @property
    def race(self):
        """Returns race"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[4]//text()')
        return self._strip(value)

    @property
    def weight(self):
        """Returns weight"""
        value = self.tree.xpath('//div[@id="mainContent"]/table[1]/tr[2]/td[7]//text()')
        return self._strip(value)
