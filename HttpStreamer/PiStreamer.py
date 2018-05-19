'''
Created on May 19, 2018

References:
    [1] https://developer.apple.com/streaming/
    [2] https://developer.apple.com/library/content/technotes/tn2288/_index.html
    

@author: navendusinha
'''

import os

class PiStreamer(object):
    '''
    classdocs
    '''

    outdir = None
    def __init__(self, outdir):
        '''
        Constructor
        '''
        self.outdir = os.path.join(os.getcwd(), 'video')
        
        
        