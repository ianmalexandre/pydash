# -*- coding: utf-8 -*-
"""
@author: Ian Moura Alexandre (ian.mouraal@gmail.com)
@author: Gabrel Vieira Arimatéa () 
@author: Felipe Calassa Albuquerque ()

@description: PyDash Project

An implementation example of a Fuzzy R2A Algorithm.

the quality list is obtained with the parameter of
handle_xml_response() method and the choice
is made inside of handle_segment_size_request(),
before sending the message down.

In this algorithm it's used a Fuzzy controller to
define the video's qualitty.
"""
import skfuzzy as fuzz
from numpy import mean, floor
from skfuzzy import control as ctrl
import time

# from player.parser import *
from player.parser import parse_mpd
from r2a.ir2a import IR2A
from r2a.utils.fuzzyfication import fuzzyficationBufferingTime as fuzzyfy
from r2a.utils.createRules import createRules


class R2AFuzzy(IR2A):

    def __init__(self, id):
        IR2A.__init__(self, id)
        self.parsed_mpd = ''
        self.qi = []
        (self.bufferTime, self.diffBufferTime, self.output) = fuzzyfy()
        self.rules = createRules(self.bufferTime,
                                 self.diffBufferTime,
                                 self.output)
        self.quality_ctrl = ctrl.ControlSystem(self.rules)
        self.throughputs = []
        self.request_time = 0.0

    def createSim(self, bufferTime, diffBufferTime):
        qi = ctrl.ControlSystemSimulation(self.quality_ctrl)
        qi.input['bufferTime'] = bufferTime
        qi.input['diffBufferTime'] = diffBufferTime

        qi.compute()

        return qi.output['output']

    def handle_xml_request(self, msg):
        self.request_time = time.perf_counter()
        self.send_down(msg)

    def handle_xml_response(self, msg):
        self.parsed_mpd = parse_mpd(msg.get_payload())
        self.qi = self.parsed_mpd.get_qi()

        # Calculo da vazão do segmento atual
        t = time.perf_counter() - self.request_time
        self.throughputs.append(msg.get_bit_length() / t)

        self.send_up(msg)

    def handle_segment_size_request(self, msg):
        time_list = self.whiteboard.get_playback_segment_size_time_at_buffer()

        # Se o tamanho da lista for menor que 2,
        # manda a menor resolução possível
        if len(time_list) < 2:
            msg.add_quality_id(self.qi[0])
            self.send_down(msg)
            return

        time_segment = time_list[-1]
        delta_time = time_segment - time_list[-2]

        # Defuzzyficação
        compute_fuzzy = self.createSim(time_segment, delta_time)
        print(f'Resultado do computing {compute_fuzzy}')

        if len(self.throughputs) < 10:
            available_throughtput = mean(self.throughputs)
        else:
            available_throughtput = self.throughputs[-9:] / 10
        predictBitrate = compute_fuzzy*available_throughtput
        print(f'the new bitrate is {predictBitrate}')

        # Encontra o elemento mais próximo do bitrate desejado
        newQi = min(self.qi, key=lambda x:abs(x - predictBitrate))

        # Encontra o index
        newQi = self.qi.index(newQi)
        print('Nova qualidade', newQi)
        
        msg.add_quality_id(self.qi[newQi])
        self.send_down(msg)

    def handle_segment_size_response(self, msg):
        self.send_up(msg)

    def initialize(self):
        pass

    def finalization(self):
        pass
