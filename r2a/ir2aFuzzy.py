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
from utils.fuzzyfication import fuzzyficationBufferingTime as fuzzyfy


class IR2AFuzzy(IR2A):

    def __init__(self):
        (self.buffTime, self.diffBuffTime, self.output) = fuzzyfy()
