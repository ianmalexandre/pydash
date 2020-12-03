# -*- coding: utf-8 -*-
"""
@author: Marcos F. Caetano (mfcaetano@unb.br) 03/11/2020

@description: PyDash Project

An implementation example of a FIXED R2A Algorithm.

the quality list is obtained with the parameter of
handle_xml_response() method and the choice
is made inside of handle_segment_size_request(),
before sending the message down.

In this algorithm the quality choice is always the same.
"""

from player.parser import *
from r2a.ir2a import IR2A
from r2a.utils.fuzzyfication import fuzzyficationBufferingTime as fuzzyfy
from r2a.utils.createRules import createRules
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class IR2AFuzzy(IR2A):

    def __init__(self, id):
        (self.bufferTime, self.diffBufferTime, self.output) = fuzzyfy()
        self.rules = createRules(self.bufferTime, self.diffBufferTime, self.output)
        self.quality_ctrl = ctrl.ControlSystem(self.rules)

    def createSim(self):
        qi = ctrl.ControlSystemSimulation(self.quality_ctrl)
        qi.input['bufferTime'] = 25.0
        qi.input['diffBufferTime'] = 0

        qi.compute()

        print(qi.output['output'])
        self.output.view(sim=qi)

    def handle_xml_request(self, msg):
        pass

    def handle_xml_response(self, msg):
        pass

    def handle_segment_size_request(self, msg):
        pass

    def handle_segment_size_response(self, msg):
        pass

    def initialize(self):
        pass

    def finalization(self):
        pass
