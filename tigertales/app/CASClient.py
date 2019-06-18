import sys, os, cgi, urllib, re
from django.conf import settings

class CASClient:

	def __init__(self):
		self.cas_url = 'https://fed.princeton.edu/cas/'

	def Authenticate(self, request):
		# If the request contains a login ticket, try to validate it
		if 'ticket' in request.GET:
			netid = self.Validate(request.GET['ticket'])
			if netid != None:
				return {'net_id': netid}
		# No valid ticket; redirect the browser to the login page to get one
		login_url = self.cas_url + 'login' + '?service=' + urllib.quote(self.ServiceURL())
		print login_url
		print 'Location: ' + login_url
		print 'Status-line: HTTP/1.1 307 Temporary Redirect'
		print ""
		return {'login_url': login_url}

	def Validate(self, ticket):
		val_url = self.cas_url + "validate" + '?service=' + urllib.quote(self.ServiceURL()) + '&ticket=' + urllib.quote(ticket)
		r = urllib.urlopen(val_url).readlines()   # returns 2 lines
		if len(r) == 2 and re.match("yes", r[0]) != None:
			return r[1].strip()
		return None

	def ServiceURL(self):
		if os.environ.has_key('REQUEST_URI'):
			ret = 'http://' + os.environ['HTTP_HOST'] + os.environ['REQUEST_URI']
			ret = re.sub(r'ticket=[^&]*&?', '', ret)
			ret = re.sub(r'\?&?$|&$', '', ret)
			return ret
		elif settings.DEBUG:
			print "ok, here now"
			return "http://localhost:8000/app/login"
		return "something is badly wrong"

def main():
	print "CASClient does not run standalone"

if __name__ == '__main__':
	main()
