import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# target buffering time
tb = 35.0


def fuzzyficationBufferingTime():

    """
        Function responsible for modeling the
        input and output variables for the fuzzy
        control

        Returns:
            (ctrl.Antecedent, ctrl.Antecedent, ctrl.Antecedent)
            - buffering time, diference between buffering times
            and output fuzzyfication modeling
    """
    buffTime = ctrl.Antecedent(np.arange(0, 150, 0.1), 'buffTime')
    diffBuffTime = ctrl.Antecedent(np.arange(-40, 150, 0.1), 'diffBuffTime')
    output = ctrl.Antecedent(np.arange(0, 3, 0.1), 'diffBuffTime')

    buffTime['short'] = fuzz.trapmf(buffTime.universe,
                                    [-6, -2, 2*tb/3, tb])
    buffTime['close'] = fuzz.trapmf(buffTime.universe,
                                    [2*tb/3, tb, tb+1, 4*tb])
    buffTime['long'] = fuzz.trapmf(buffTime.universe,
                                   [tb, 4*tb, 4*tb+20, 4*tb+30])

    diffBuffTime['falling'] = fuzz.trapmf(diffBuffTime.universe,
                                          [-40, -35, -2*tb/3, 0])
    diffBuffTime['steady'] = fuzz.trimf(diffBuffTime.universe,
                                        [-2*tb/3, 0, 4*tb])
    diffBuffTime['rising'] = fuzz.trapmf(diffBuffTime.universe,
                                         [0, 4*tb, 4*tb + 20, 4*tb + 30])

    output['reduce'] = fuzz.trapmf(output.universe,
                                   [-6, -2, 0.25, 0.5])
    output['smallReduce'] = fuzz.trimf(output.universe,
                                       [0.25, 0.5, 1])
    output['noChange'] = fuzz.trimf(output.universe,
                                    [0.5, 1, 1.5])
    output['smallIncrease'] = fuzz.trimf(output.universe,
                                         [1, 1.5, 2])
    output['Increase'] = fuzz.trapmf(output.universe,
                                     [1.5, 2, 3, 4])

    return (buffTime, diffBuffTime, output)


# (buffTime, diffBuffTime, output) = fuzzyficationBufferingTime()

# buffTime.view()
# diffBuffTime.view()
# output.view()
