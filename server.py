'''
Python Modules Version Specification Given in requirement.txt
'''
import cherrypy
import ConfigParser
import json
import os
import Assembler

class Server():

    @cherrypy.expose
    def index(self):
        '''
            Render the index.html File for the Interface for the Client
        '''

        return open(os.path.join(os.path.join(os.path.abspath("."), u"resources"), u'index.html'))


    @cherrypy.expose
    def generateCode(self):
        received_data = cherrypy.request.body.read()
        try:
            decoded_data = json.loads(received_data)
            code = decoded_data['code']
            filename = decoded_data['filename']
        except KeyError:
            return json.dumps({"status":2, "message":"Invalid Data Sent to the Server"})

        try:
            codeRequest  = Assembler()
            data_sent = codeRequest.assemble()
        except KeyError:
            data_sent = {'status': "failed"}
        return json.dumps(data_sent)


'''
    Setting up the Server with Specified Configuration
'''
if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read('server.conf')
    cherrypy.server.socket_host = config.get('server', 'host')
    cherrypy.server.socket_port = int(config.get('server', 'port'))
    conf = {
        '/':{
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/resources': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './resources'
        }
    }
cherrypy.quickstart(Server(), '/', conf)
