import urllib
import urllib.request
from bs4 import BeautifulSoup
import datetime

class Investing():
	def __init__(self):
		self.req = urllib.request.Request('http://ru.investing.com/economic-calendar/')
		self.req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
		self.result = []

	def news(self):
		response = urllib.request.urlopen(self.req)
		html = response.read()
		
		soup = BeautifulSoup(html, "html.parser")

		table = soup.find('table', {"id": "economicCalendarData"})
		tbody = table.find('tbody')
		rows = tbody.findAll('tr', {"class": "js-event-item"})
		news = {'time': None, 'country': None, 'impact': None, 'url': None, 'name': None, 'bold': None, 'fore': None, 'prev': None, 'signal': None}
		
		for row in rows:
			#print row.attrs['data-event-datetime']
			news['time'] = int(datetime.datetime.strptime(row.attrs['data-event-datetime'], '%Y/%m/%d %H:%M:%S').strftime('%s'))

		for tr in rows:
			cols = tr.find('td', {"class": "flagCur"})
			flag = cols.find('span')
			#print (flag.get('title'))
			news['country'] = flag.get('title')

			impact = tr.find('td', {"class": "sentiment"})
			bull = impact.findAll('i', {"class": "grayFullBullishIcon"})
			#print len(bull)
			news['impact'] = len(bull)

			event = tr.find('td', {"class": "event"})
			a = event.find('a')
			#print "http://ru.investing.com"+a['href']
			news['url'] = "http://ru.investing.com"+a['href']
			
			#print a.text.strip()
			news['name'] = a.text.strip()

			bold = tr.find('td', {"class": "bold"})
			#print bold.text
			if bold.text != '':
				news['bold'] = bold.text.strip()
			else:
				news['bold'] = ''

			fore = tr.find('td', {"class": "fore"})
			#print fore.text
			news['fore'] = fore.text.strip()

			prev = tr.find('td', {"class": "prev"})
			#print prev.text
			news['prev'] = prev.text.strip()

			if "blackFont" in bold['class']:
				#print '?'
				news['signal'] = "?"

			elif "redFont" in bold['class']:
				#print '-'
				news['signal'] = "-"

			elif "greenFont" in bold['class']:
				#print '+'
				news['signal'] = "+"

			self.result.append(news)

		return self.result


