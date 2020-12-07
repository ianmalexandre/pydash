import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl



def fuzzyficationBufferingTime():
    """
        Function responsible for modeling the
        input and output variables for the fuzzy
        control

        Returns:
            (ctrl.Antecedent, ctrl.Antecedent, ctrl.Consequent)
            - buffering time, diference between buffering times
            and output fuzzyfication modeling
    """
    # target buffering time
    tb = 35.0
    bufferTime = ctrl.Antecedent(np.arange(0, 4*tb+110, 0.1), 'bufferTime')
    diffBufferTime = ctrl.Antecedent(np.arange(-tb-10, 4*tb+110, 0.1), 'diffBufferTime')
    output = ctrl.Consequent(np.arange(0, 3, 0.1), 'output')

    bufferTime['short'] = fuzz.trapmf(bufferTime.universe,
                                    [-50, -40, 2*tb/3, tb])
    bufferTime['close'] = fuzz.trapmf(bufferTime.universe,
                                    [2*tb/3, tb, tb+1, 4*tb])
    bufferTime['long'] = fuzz.trapmf(bufferTime.universe,
                                   [tb, 4*tb, 4*tb+100, 4*tb+110])

    diffBufferTime['falling'] = fuzz.trapmf(diffBufferTime.universe,
                                          [-tb-80, -tb-50, -2*tb/3, 0])
    diffBufferTime['steady'] = fuzz.trimf(diffBufferTime.universe,
                                        [-2*tb/3, 0, 4*tb])
    diffBufferTime['rising'] = fuzz.trapmf(diffBufferTime.universe,
                                         [0, 4*tb, 4*tb + 100, 4*tb + 110])

    output['reduce'] = fuzz.trapmf(output.universe,
                                   [-10, -7, 0.25, 0.5])
    output['smallReduce'] = fuzz.trimf(output.universe,
                                       [0.25, 0.5, 1])
    output['noChange'] = fuzz.trimf(output.universe,
                                    [0.5, 1, 1.5])
    output['smallIncrease'] = fuzz.trimf(output.universe,
                                         [1, 1.5, 2])
    output['increase'] = fuzz.trapmf(output.universe,
                                     [1.5, 2, 7, 10])

    return (bufferTime, diffBufferTime, output)


(bufferTime, diffBufferTime, output) = fuzzyficationBufferingTime()

bufferTime.view()
diffBufferTime.view()
output.view()
