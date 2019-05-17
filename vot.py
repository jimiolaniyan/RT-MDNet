"""
\file vot.py

@brief Python utility functions for VOT integration

@author Luka Cehovin, Alessio Dore

@date 2016

"""

import sys
import copy
import logging

LOG = "/tmp/ccd.log"
logging.basicConfig(filename=LOG, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

import collections

try:
    import trax
except ImportError:
    raise Exception('TraX support not found. Please add trax module to Python path.')

Rectangle = collections.namedtuple('Rectangle', ['x', 'y', 'width', 'height'])
Point = collections.namedtuple('Point', ['x', 'y'])
Polygon = collections.namedtuple('Polygon', ['points'])

class VOT(object):
    """ Base class for Python VOT integration """
    def __init__(self, region_format, channels=None):
        """ Constructor

        Args:
            region_format: Region format options
        """
        assert(region_format in [trax.Region.RECTANGLE, trax.Region.POLYGON])

        if channels is None:
            channels = ['color']
        elif channels == 'rgbd':
            channels = ['color', 'depth']
        elif channels == 'rgbt':
            channels = ['color', 'ir']
        elif channels == 'ir':
            channels = ['ir']
        else:
            raise Exception('Illegal configuration {}.'.format(channels))

        self._trax = trax.Server([region_format], [trax.Image.PATH], channels)

        request = self._trax.wait()
        assert(request.type == 'initialize')
        if isinstance(request.region, trax.Polygon):
            self._region = Polygon([Point(x[0], x[1]) for x in request.region])
        else:
            self._region = Rectangle(*request.region.bounds())
        self._image = [str(x) for k, x in request.image.items()]
        if len(self._image) == 1:
            self._image = self._image[0]
        self._trax.status(request.region)

    def region(self):
        """
        Send configuration message to the client and receive the initialization
        region and the path of the first image

        Returns:
            initialization region
        """

        return self._region

    def report(self, region, confidence = None):
        """
        Report the tracking results to the client

        Arguments:
            region: region for the frame
        """
        assert(isinstance(region, Rectangle) or isinstance(region, Polygon))
        if isinstance(region, Polygon):
            tregion = trax.Polygon.create([(x.x, x.y) for x in region.points])
        else:
            tregion = trax.Rectangle.create(region.x, region.y, region.width, region.height)
        properties = {}
        if not confidence is None:
            properties['confidence'] = confidence
        self._trax.status(tregion, properties)

    def frame(self):
        # logging.debug('In frame with self: %s', self)
	"""
        Get a frame (image path) from client

        Returns:
            absolute path of the image
        """
	#att = hasattr(self, '_image')
        #logging.debug('Hasattr: %s', att)

        if hasattr(self, "_image"):
            image = self._image
            del self._image
            return image[18:-1]

        # logging.debug('begin trax.wait')
	# logging.debug('_trax is: %s', self._trax)

        request = self._trax.wait()

        # typ = request.type
        # logging.debug('frame: %s', typ)

        if request.type == 'frame':
            image = [str(x) for k, x in request.image.items()]
            # logging.info('image in loop is: %s', image)
            if len(image) == 1:
                return image[0][18:-1]
            return tuple(image)
        else:
            return None


    def quit(self):
        if hasattr(self, '_trax'):
            self._trax.quit()

    def __del__(self):
        self.quit()

