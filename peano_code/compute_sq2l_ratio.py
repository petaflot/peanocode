# Copyright (C) 2016 Konstantin Bauman <kbauman@yandex.ru>
# Licensed under the GNU LGPL v3 - http://www.gnu.org/licenses/lgpl.html

from peano_code.curve import curve_step
from peano_code.fraction import fraction_pair


'''
Definition:
    compute_sq_ratio(d0, dnplus1, C, N) - is a function for calculating 
    the square-to-linear ratio for the specified Peano curve.
    
    The codes defining Peano curves introduced in 
        Bauman K., "One-side peano curves of fractal genus 9"
        Proceedings of the Steklov Institute of Mathematics 275 (1), 47-59

Attributes:
    d0       -  code of the basic step of the curve. 
    dnplus1  -  code for constructing the next step of the curve based on the current one. 
    sq2l_lower_bound  -  a lower boundary on the square-to-linear ratio. It is used for reducing calculations. 
    N        -  Peano curve construction step number. The script constructs the specified Peano curve 
                up to the N-th step and calculates square-to-linear ratios between all pairs of corners
                on this step.
    
Return:
    a list of variables describing the maximum square-to-linear ratio 
    and the example of pair of points reaching this maximum.
    [
        0: (float) maximum identified square-to-linear ratio
        1: (int) number of construction step
        2: (complex) coordinate of the first point on the complex plane
        3: (float) time (or linear coordinate) of the 1st point
        4: (complex) coordinate of the 2nd point on the complex plane
        5: (float) time (or linear coordinate) of the 2nd point
        6: (int) the overall time in the interval
        7: (int) the side of the constructed square
    ]
    
    Example:
        [6.0, 5, (8+16j), 490.66, (24+16j), 533.33, 1024, 32]


'''


def compute_sq2l_ratio(d0, dnplus1, N = 5, sq2l_lower_bound = 5.0, logger=None):
    'create curve'
    curve = curve_step(d0, dnplus1)
    'construct second step of the curve'
    curve.make_next()
    'validate curve and calculate time values'
    if not curve.curve_validation():
        return 0
    'create set of fractions on the second construction step'
    f_set = curve.make_fractions_set()
    
    
    step_fraction_pairs = {}
    'step number -> list of fraction pairs'
    for fraction1_num in range(len(f_set)):
        for fraction2_num in range(fraction1_num + 1, len(f_set)):
            if f_set[fraction1_num].n not in step_fraction_pairs:
                step_fraction_pairs[f_set[fraction1_num].n] = list()
            step_fraction_pairs[f_set[fraction1_num].n].append(fraction_pair(f_set[fraction1_num], f_set[fraction2_num]))
    
    
    for step_number in range(N):
        if step_number not in step_fraction_pairs:
            'skip step if there is no fraction pairs to process'
            continue
        
        'iterate over fraction pairs'
        for f_pair in step_fraction_pairs[step_number]:
            '''
            estimate maximum square-to-linear ratio between points from fraction x and fraction y,
            if the result is higher than specified lower bound:
                go deeper and create all pairs of sub-fractions on the next step. 
            '''
            next_step_fraction_pairs = f_pair.decide(sq2l_lower_bound)
            if not next_step_fraction_pairs:
                continue
            if next_step_fraction_pairs[0].n not in step_fraction_pairs:
                    step_fraction_pairs[next_step_fraction_pairs[0].n] = list()
            step_fraction_pairs[next_step_fraction_pairs[0].n] += next_step_fraction_pairs
            #print j.n,temp[0].n
        del step_fraction_pairs[step_number]
        
    'calculate maximum square-to-linear ratio for the rest of the fraction pairs on the Nth step'
    curve_sq2l_ratio = [0.0]
    for f_pair in step_fraction_pairs[N]:
        sq_ratio = f_pair.maximum_sq2l_ratio()
        if sq_ratio[0] > curve_sq2l_ratio[0]:
            curve_sq2l_ratio = sq_ratio
            
    return curve_sq2l_ratio