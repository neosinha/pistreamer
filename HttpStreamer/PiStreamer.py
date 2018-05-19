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
    vwriter = None  
    videodir = None 
    
    seq=0
    tscount = 0 
    
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
        
        self.videodir = os.path.join(self.staticdir, 'videos')
        
        
        
        if self.camera: 
            print "Camera is ready.."
        
        
        self.videodir = os.path.join(os.getcwd(), 'video')
        if os.path.exists(self.videodir):
            print("Creating directory for streaming video, {}".format(self.videodir))
            os.mkdir(self.videodir)
        
        self.capVideo()
    
    
    def capVideo(self):
        """
        Increment tscount every second
        
        """
        print "Starting camera"
        self.tscount = 0
        # fourcc = cv2.VideoWriter_fourcc(*'MPV4')
        # ut = cv2.VideoWriter('output.avi', -1, 20.0, (640,480))
        vfile = os.path.join(self.videodir, 'video-{}.mp4'.format(self.tscount))
        self.vwriter = cv2.VideoWriter(vfile,-1, 20.0, (640,480))
        while True: 
            ret, self.frame = self.camera.read()
            self.gframe = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Face", self.frame)
            
            self.vwriter(self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
       
        self.camera.release()
        self.vwriter.release()
        
    
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
    
    ap.add_argument("-i", "--ipaddress", required=True,
                    help="IP Address to start HTTPServer")
    
    
    ap.add_argument("-w", "--staticdir", required=False, 
                     help = "Static directory which contains the WWW folder")
    
    

    args = vars(ap.parse_args())
    portnum = int(args["port"])
    ipadd = args["ipaddress"]
    
    staticdir = os.path.join(os.getcwd(), "www")
    if args["staticdir"]:
        staticdir = args ["staticdir"]
    
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
    print "Starting HTTPServer on %s, serving pages from %s" % (str(portnum), staticdir)
    
    Streamer.quickstart(PiStreamer(staticdir=staticdir), '/', conf)
    






 