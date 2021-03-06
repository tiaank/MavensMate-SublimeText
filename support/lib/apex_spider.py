import urllib2
from BeautifulSoup import BeautifulSoup
import pprint
import json
import os

# types = [
#   'blob', 'string', 'set', 'list', 'date', 'datetime', 'boolean', 'double', 'id', 'integer', 'long', 'time', 'map', 'enum', 'apexpages', 'approval', 'limits', 'math', 'search', 'system', 'test', 'timezone', 'type', 'userinfo'
# ]

types = [
  'blob', 'string', 'date', 'datetime', 'boolean', 'double', 'id', 'integer', 'long', 'time', 'enum', 'apexpages', 'approval', 'limits', 'math', 'search', 'system', 'test', 'timezone', 'type', 'userinfo'
]

##userinfo table is 
#system, userinfo, math, approval, limits, test, selectoption


for t in types:
    print 'processing --> ', t
    d = {
        "instance_methods" : [

        ],
        "static_methods" : [

        ]
    }

    soup = BeautifulSoup(urllib2.urlopen('http://www.salesforce.com/us/developer/docs/apexcode/Content/apex_methods_system_'+t+'.htm').read())

    tables = soup('table', {'class' : 'featureTable'})

    #static
    for row in tables[0].tbody('tr'):
        #print "--row--"
        tds = row('td')
        method_name = tds[0].find('samp').string
        if method_name == None:
            method_name = tds[0].find('samp').text.replace('\n', '')
        try:
            contents = tds[1].contents
            arguments = ''
            #print len(contents)
            if len(contents) == 2:
                arguments = contents[0].replace(' ', '').replace('&lt;', '_').replace('\n', '').replace('&gt;', '_').strip()+"_"+contents[1].string
            elif len(contents) > 2:
                args=[]
                args.append(contents[0].replace(' ', '').replace('&lt;', '_').replace('\n', '').replace('&gt;', '_').strip()+"_"+contents[1].string.lower())
                for i, c in enumerate(contents):
                    if i > 1:
                        #print 'c: ', c.contents
                        inner_contents = c.contents
                        args.append(inner_contents[0].replace(' ', '').replace('&lt;', '_').replace('\n', '').replace('&gt;', '_').strip()+"_"+inner_contents[1].string.lower())

                arguments = ', '.join(args)
            #print 'args: ', arguments
            #arguments += "_"+tds[1].find('var').string
        except Exception, e:
            print e
            arguments = ''

        return_type = tds[2].string
        try:
            description = tds[3].string
        except:
            description = 'None'

        d["static_methods"].append(
          "{0}({1})".format(method_name, arguments)
        )

    if len(tables) > 1:
        try:
            for row in tables[1].tbody('tr'):
                #print "--row--"
                tds = row('td')
                method_name = tds[0].find('samp').string
                if method_name == None:
                    method_name = tds[0].find('samp').text.replace('\n', '')
                try:
                    contents = tds[1].contents
                    arguments = ''
                    #print len(contents)
                    if len(contents) == 2:
                        arguments = contents[0].replace(' ', '').replace('&lt;', '_').replace('&gt;', '_').replace('\n', '').strip()+"_"+contents[1].string
                    elif len(contents) > 2:
                        args=[]
                        args.append(contents[0].replace(' ', '').replace('&lt;', '_').replace('&gt;', '_').replace('\n', '').strip()+"_"+contents[1].string.lower())
                        for i, c in enumerate(contents):
                            if i > 1:
                                #print 'c: ', c.contents
                                inner_contents = c.contents
                                args.append(inner_contents[0].replace(' ', '').replace('&lt;', '_').replace('\n', '').replace('&gt;', '_').strip()+"_"+inner_contents[1].string.lower())

                        arguments = ', '.join(args)
                except Exception, e:
                    print e
                    arguments = ''

                return_type = tds[2].string
                try:
                    description = tds[3].string
                except:
                    description = 'None'

                d["instance_methods"].append(
                  "{0}({1})".format(method_name, arguments)
                )
        except:
            pass

    file_body = json.dumps(d, sort_keys=False, indent=4)
    src = open(os.path.join(os.path.dirname(__file__), 'apex', t+'.json'), 'w')
    src.write(file_body)
    src.close()
