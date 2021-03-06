#
#    Copyright (c) 2010 Min Ragan-Kelley
#
#    This file is part of pyzmq.
#
#    pyzmq is free software; you can redistribute it and/or modify it under
#    the terms of the Lesser GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    pyzmq is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    Lesser GNU General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import time

import zmq
from zmq import devices
from zmq.tests import BaseZMQTestCase


#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------


class TestDevice(BaseZMQTestCase):

    def test_device_types(self):
        # a = self.context.socket(zmq.SUB)
        for devtype in (zmq.STREAMER, zmq.FORWARDER, zmq.QUEUE):
            dev = devices.Device(devtype, zmq.PAIR,zmq.PAIR)
            self.assertEquals(dev.device_type, devtype)
            del dev
        # del a
    
    def test_device_attributes(self):
        # a = self.context.socket(zmq.SUB)
        # b = self.context.socket(zmq.PUB)
        dev = devices.Device(zmq.FORWARDER, zmq.SUB, zmq.PUB)
        self.assert_(dev.in_type == zmq.SUB)
        self.assert_(dev.out_type == zmq.PUB)
        self.assertEquals(dev.device_type, zmq.FORWARDER)
        self.assertEquals(dev.daemon, True)
        # del a
        del dev
    
    def test_tsdevice_attributes(self):
        dev = devices.Device(zmq.QUEUE, zmq.SUB, zmq.PUB)
        self.assertEquals(dev.in_type, zmq.SUB)
        self.assertEquals(dev.out_type, zmq.PUB)
        self.assertEquals(dev.device_type, zmq.QUEUE)
        self.assertEquals(dev.daemon, True)
        del dev
        
    
    def test_single_socket_forwarder_connect(self):
        dev = devices.ThreadDevice(zmq.FORWARDER, zmq.REP, -1)
        req = self.context.socket(zmq.REQ)
        port = req.bind_to_random_port('tcp://127.0.0.1')
        dev.connect_in('tcp://127.0.0.1:%i'%port)
        dev.start()
        time.sleep(.25)
        msg = 'hello'
        req.send(msg)
        self.assertEquals(msg, req.recv())
        del dev
        del req
        dev = devices.ThreadDevice(zmq.FORWARDER, zmq.REP, -1)
        req = self.context.socket(zmq.REQ)
        port = req.bind_to_random_port('tcp://127.0.0.1')
        dev.connect_out('tcp://127.0.0.1:%i'%port)
        dev.start()
        time.sleep(.25)
        msg = 'hello again'
        req.send(msg)
        self.assertEquals(msg, req.recv())
        del dev
        del req
        
    def test_single_socket_forwarder_bind(self):
        dev = devices.ThreadDevice(zmq.FORWARDER, zmq.REP, -1)
        req = self.context.socket(zmq.REQ)
        port = 12345
        req.connect('tcp://127.0.0.1:%i'%port)
        dev.bind_in('tcp://127.0.0.1:%i'%port)
        dev.start()
        time.sleep(.25)
        msg = 'hello'
        req.send(msg)
        self.assertEquals(msg, req.recv())
        del dev
        del req
        dev = devices.ThreadDevice(zmq.FORWARDER, zmq.REP, -1)
        req = self.context.socket(zmq.REQ)
        port = 12346
        req.connect('tcp://127.0.0.1:%i'%port)
        dev.bind_in('tcp://127.0.0.1:%i'%port)
        dev.start()
        time.sleep(.25)
        msg = 'hello again'
        req.send(msg)
        self.assertEquals(msg, req.recv())
        del dev
        del req
