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
from base.whiteboard import Whiteboard

class R2AFuzzy(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''
        self.qi = []
        (self.bufferTime, self.diffBufferTime, self.output) = fuzzyfy()
        self.rules = createRules(self.bufferTime, self.diffBufferTime, self.output)
        self.quality_ctrl = ctrl.ControlSystem(self.rules)
        self.request_time = time.perf_counter()

    def createSim(self, bufferTime, diffBufferTime):
        qi = ctrl.ControlSystemSimulation(self.quality_ctrl)
        qi.input['bufferTime'] = bufferTime
        qi.input['diffBufferTime'] = diffBufferTime

        qi.compute()

        return qi.output['output']

        # print(qi.output['output'])
        # self.output.view(sim=qi)

    def handle_xml_request(self, msg):
        self.send_down(msg)

    def handle_xml_response(self, msg):
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        time_list = self.whiteboard.get_playback_segment_size_time_at_buffer()
        if len(time_list) < 1:
            time_list = (35, 1)
        elif len(time_list) == 1:
            time_list = (35, time_list[0])
        time_segment = time_list[-1]
        delta_time = time_segment - time_list[-2]

        compute_fuzzy = self.createSim(time_segment, delta_time)
        print(f'Resultado do computing {compute_fuzzy}')

        msg.add_quality_id(self.qi[10])
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass
