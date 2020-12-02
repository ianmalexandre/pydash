import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def createRules(bufferTime, diffBufferTime, output):
    rules = []
    rules.append(ctrl.Rule(bufferTime['short'] & diffBufferTime['falling'],
                      output['reduce']))
    rules.append(ctrl.Rule(bufferTime['close'] & diffBufferTime['falling'],
                      output['smallReduce']))
    rules.append(ctrl.Rule(bufferTime['long'] & diffBufferTime['falling'],
                      output['noChange']))
    rules.append(ctrl.Rule(bufferTime['short'] & diffBufferTime['steady'],
                      output['smallReduce']))
    rules.append(ctrl.Rule(bufferTime['close'] & diffBufferTime['steady'],
                      output['noChange']))
    rules.append(ctrl.Rule(bufferTime['long'] & diffBufferTime['steady'],
                      output['smallIncrease']))
    rules.append(ctrl.Rule(bufferTime['short'] & diffBufferTime['rising'],
                      output['noChange']))
    rules.append(ctrl.Rule(bufferTime['close'] & diffBufferTime['rising'],
                      output['smallIncrease']))
    rules.append(ctrl.Rule(bufferTime['long'] & diffBufferTime['rising'],
                      output['increase']))

    # rules[0].view()
    return rules
