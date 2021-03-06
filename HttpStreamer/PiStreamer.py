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
import subprocess

from picamera import PiCamera
import time
import datetime 
from time import sleep


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
    
    tscount = 0 # video file sequence count
    plcount = 0 # play list count
    
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
        
        self.camera = PiCamera()
        self.videodir = os.path.join(self.staticdir, 'videos')
        
        
        
        if self.camera: 
            print "Camera is ready.."
        
        
        # self.videodir = os.path.join(os.getcwd(), 'video')
        if not os.path.exists(self.videodir):
            print("Creating directory for streaming video, {}".format(self.videodir))
            os.mkdir(self.videodir)
        
        
        # self.capVideo()
        self.createPlayListVideo(numsecs=60)
        
    
    def createPlayListVideo(self, numsecs=60):
        """
        Capture num seconds of video
        + numsec: seconds
        """
        stime = self.epoch()
        etime = stime + numsecs*1000
        
        self.tscount = 0
        while self.epoch() < etime :
            print("Start Video EL[{}], {}, {}, {}".format(self.tscount, 
                                self.getts(), 
                                stime, 
                                etime))
            self.capVideo()
            self.postProcess()
            # change the tscount file
            self.tscount += 1
            print("Finish Video EL[{}], {}, {}, {}".format(self.tscount, 
                                self.getts(), 
                                stime, 
                                etime))
    
    def getts(self):
        """
        Get formatted time-stamp
        """
        ts = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        return ts
    
    def capVideo(self):
        """
        Increment tscount every second
        
        """
        print "Starting camera"
        self.vfile = os.path.join(self.videodir, 'video{}.h264'.format(self.tscount) )
        self.camera.start_recording(self.vfile)
        sleep(10)
        self.camera.stop_recording()
   
    def postProcess(self):
        """
        Post process video
        MP4Box -add video.h264 video.mp4
        """
        h264 = os.path.join(self.videodir, 'video{}.mp4'.format(self.tscount))
        ps = subprocess.Popen(('MP4Box', '-add', self.vfile, h264), stdout=subprocess.PIPE)
        # output = subprocess.check_output(('grep', 'process_name'), stdin=ps.stdout)
        ps.wait()
        # remove file
        
        os.remove(self.vfile)
        
    
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
    






 