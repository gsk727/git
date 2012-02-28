import urllib2



req = urllib2.Request('http://8.8.8.8')
try:
    response = urllib2.urlopen(req, timeout= 10)

    the_page = response.read()
    print the_page
except:
    print "timeout"

