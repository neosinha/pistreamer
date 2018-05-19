'''
Created on May 19, 2018

References:
    [1] https://developer.apple.com/streaming/
    [2] https://developer.apple.com/library/content/technotes/tn2288/_index.html
    

@author: navendusinha
'''

import os
import argparse
import cherrypy as Streamer

import cv2


class PiStreamer(object):
    '''
    classdocs
    '''


    m3u8 = []
    staticdir = None
    
    camera = None 
    def __init__(self, staticdir):
        '''
        Constructor
        '''
        self.staticdir = staticdir
        
        self.m3u8.append("#EXTM3U")
        self.m3u8.append("#EXT-X-TARGETDURATION:10")
        self.m3u8.append("#EXT-X-VERSION:3")
        self.m3u8.append("#EXT-X-MEDIA-SEQUENCE:0")
        self.m3u8.append("#EXT-X-PLAYLIST-TYPE:VOD")
        
        self.camera = cv2.VideoCapture(0)
        if self.camera: 
            print "Camera is ready.."
        
        
        self.outdir = os.path.join(os.getcwd(), 'video')
        
    
    
    def epoch(self):
        """
        Returns the 
        """
        ts = int(round(time.time() * 1000))
        
        return ts

    @Streamer.expose
    def index(self):
        """
        """
        return open(os.path.join(self.staticdir, "index.html"))
        
    
    def updatem3u8(self):
        """
        Update the m3u8 file
        """
        
    




if __name__ == '__main__':
    ap = argparse.ArgumentParser()  
    
    ap.add_argument("-p", "--port", required=True,
                help="Port number for Streaming Server")

    ap.add_argument("-d", "--odir", required=False,
                help="Directory for storing videos")
    
    ap.add_argument("-i", "--ipaddress", required=True,
                    help="IP Address to start HTTPServer")
    
    
    ap.add_argument("-w", "--staticdir", required=False, 
                     help = "Static directory which contains the WWW folder")
    
    

    args = vars(ap.parse_args())
    portnum = int(args["port"])
    ipadd = args["ipaddress"]
    staticdir = args ["staticdir"]
    odir = args["odir"]
    
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': staticdir
        }
    }

    
    Streamer.config.update({ 'server.socket_host' : ipadd,
                              'server.socket_port': portnum,
                              'server.socket_timeout': 600,
                              'server.thread_pool' : 2,
                              'server.max_request_body_size': 0 
                              })
    print "Starting HTTPServer on %s, serving pages from " % (str(portnum), staticdir)
    
    Streamer.quickstart(PiStreamer(staticdir=staticdir), '/', conf)
    






 