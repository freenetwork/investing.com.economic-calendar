import urllib
import urllib.request
from urllib.error import HTTPError

from bs4 import BeautifulSoup
import datetime
import arrow


class Good():
	def __init__(self):
		self.value = "+"
		self.name = "good"

	def __repr__(self):
		return "<Good(value='%s')>" % (self.value)


class Bad():
	def __init__(self):
		self.value = "-"
		self.name = "bad"

	def __repr__(self):
		return "<Bad(value='%s')>" % (self.value)


class Unknown():
    def __init__(self):
        self.value = "?"
        self.name = "unknow"

    def __repr__(self):
        return "<Unknow(value='%s')>" % (self.value)


class Investing():
    def __init__(self, uri='http://ru.investing.com/economic-calendar/'):
        self.uri = uri
        self.req = urllib.request.Request(uri)
        self.req.add_header('User-Agent',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
        self.result = []

    def news(self):
        try:
            response = urllib.request.urlopen(self.req)

            html = response.read()

            soup = BeautifulSoup(html, "html.parser")

            # Find event item fields
            table = soup.find('table', {"id": "economicCalendarData"})
            tbody = table.find('tbody')
            rows = tbody.findAll('tr', {"class": "js-event-item"})

            for tr in rows:
                cols = tr.find('td', {"class": "flagCur"})
                flag = cols.find('span')

                news = {}

                news['country'] = flag.get('title')

                impact = tr.find('td', {"class": "sentiment"})
                bull = impact.findAll('i', {"class": "grayFullBullishIcon"})

                news['impact'] = len(bull)

                event = tr.find('td', {"class": "event"})
                a = event.find('a')

                news['url'] = "{}{}".format(self.uri, a['href'])
                news['name'] = a.text.strip()

                # Determite type of event
                legend = event.find('span', {"class": "smallGrayReport"})
                if legend:
                    news['type'] = "report"

                legend = event.find('span', {"class": "audioIconNew"})
                if legend:
                    news['type'] = "speech"

                legend = event.find('span', {"class": "smallGrayP"})
                if legend:
                    news['type'] = "release"

                legend = event.find('span', {"class": "sandClock"})
                if legend:
                    news['type'] = "retrieving data"

                bold = tr.find('td', {"class": "bold"})

                if bold.text != '':
                    news['bold'] = bold.text.strip()
                else:
                    news['bold'] = ''

                fore = tr.find('td', {"class": "fore"})
                news['fore'] = fore.text.strip()

                prev = tr.find('td', {"class": "prev"})
                news['prev'] = prev.text.strip()

                if "blackFont" in bold['class']:
                    # print ('?')
                    # news['signal'] = '?'
                    news['signal'] = Unknown()

                elif "redFont" in bold['class']:
                    # print ('-')
                    # news['signal'] = '-'
                    news['signal'] = Bad()

                elif "greenFont" in bold['class']:
                    # print ('+')
                    # news['signal'] = '+'
                    news['signal'] = Good()

                else:
                    news['signal'] = Unknown()

                self.result.append(news)

        except HTTPError as error:
            print("Oops... Get error HTTP {}".format(error.code))

        return self.result

if __name__ == "__main__":
	i = Investing('http://investing.com/economic-calendar/')
	print (i.news())
