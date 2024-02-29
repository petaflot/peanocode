# Copyright (C) 2016 Konstantin Bauman <kbauman@yandex.ru>
# Licensed under the GNU LGPL v3 - http://www.gnu.org/licenses/lgpl.html

import copy
import numpy as np
from peanocode.code import get_next_code

class arrow:
    def __init__(self, complex_coordinate, time):
        self.com = complex_coordinate
        self.time = time

'''
class fraction describes one fraction of the Peano curve 
on a certain construction step
'''
class fraction:
    n = 0
    left_lower_cordinates = complex(0,0)
    coord_begin = complex(0,0)
    time_begin = 0.0
    bypass = None
    dnplus1 = None
    orientation = 0
    
    
    def __init__(self, curve_list, d0, dnplus1, curve_type, code):
        self.bypass = curve_list
#         self.bypass = [copy.copy(x) for x in curve_list]
        self.d0 = d0
        self.dnplus1 = dnplus1
        self.type = curve_type
        self.code = code
        
    def print_sq(self):
        print("cord =" + str(self.left_lower_cordinates)+"; cord_begin = " + str(self.coord_begin))
        print("code = " )
        self.code.print_code()
        print(self.bypass[0].com,self.bypass[1].com,self.bypass[2].com)
        print(self.time_begin) 
        print("====")
    
    '''
    create set of sub-fractions of next construction step
    '''
    
    def next_step(self):
        next_step_curve = list()
        codes = list()
        if self.code.if_reflection == 1:
            dnplus1 = list()
            for transformation_code in self.dnplus1:
                dnplus1.append(transformation_code.copy_code())
            dnplus1.reverse()
        else:
            dnplus1 = self.dnplus1
        
        '''
        Create next step of the curve based on the current one
        and the code for constructing the next step.
        '''
        for transformation_code in dnplus1:
            'create new fraction'
            temp_curve = [copy.copy(x) for x in self.d0]
            'apply transformations'
            temp_code = get_next_code(self.code, transformation_code)
            codes.append(temp_code)
            if temp_code.if_reflection:
                temp_curve.reverse()
                if self.type == 0:
                    for arr in temp_curve:
                        arr.com = arr.com.conjugate()
            if temp_code.if_conjugate:
                for arr in temp_curve:
                    arr.com = arr.com.conjugate()
            i = copy.copy(temp_code.complex)
            while i!=1:
                for arr in temp_curve:
                    arr.com = arr.com * complex(0,1)
                i/=1j
            next_step_curve += temp_curve
            
        l = np.sqrt(len(self.dnplus1))
        sq_list = []
        
        temp_arrow_list = []
        temp_sq_start_cordinates = self.coord_begin * l
        current_coordinates = temp_sq_start_cordinates
        temp_sq_left_lower_cordinates = current_coordinates
        temp_time = self.time_begin*pow(l,2)
        
        '''
        follow the curve and create a set of sub-fractions
        '''
        i = 0 #counter for catching fractions of each three arrows
        for arrow in next_step_curve:
            temp_arrow_list.append(arrow)
            current_coordinates += arrow.com 
            if current_coordinates.real < temp_sq_left_lower_cordinates.real:
                temp_sq_left_lower_cordinates = complex(current_coordinates.real, temp_sq_left_lower_cordinates.imag)
            if current_coordinates.imag < temp_sq_left_lower_cordinates.imag:
                temp_sq_left_lower_cordinates = complex(temp_sq_left_lower_cordinates.real, current_coordinates.imag)
            i+=1
            if i%3 == 0:
                sq_list.append(fraction(temp_arrow_list, self.d0, self.dnplus1, self.type, codes[int(i/3)-1]))
                sq_list[-1].n = self.n + 1
                sq_list[-1].coord_begin = temp_sq_start_cordinates
                temp_sq_start_cordinates = current_coordinates 
                sq_list[-1].left_lower_cordinates = temp_sq_left_lower_cordinates
                temp_sq_left_lower_cordinates = current_coordinates
                sq_list[-1].time_begin = temp_time
                temp_time += 1.0
                temp_arrow_list = []
                 
        del next_step_curve
        del codes
        return sq_list




'''
class for calculating the square-to-linear ratio
between points within pair of fractions
'''
class fraction_pair:    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.n = x.n

    '''
    estimate maximum square-to-linear ratio between points from fraction x and fraction y,
    if the result is higher than specified lower bound:
        go deeper and create all pairs of sub-fractions on the next step. 
    '''
    def decide(self, sq2l_lower_bound):
        'upper bound on distance between points from fraction x and points from fraction y on the square'
        sq = abs(complex(abs(self.x.left_lower_cordinates.real - self.y.left_lower_cordinates.real)+1.0,
                         abs(self.x.left_lower_cordinates.imag - self.y.left_lower_cordinates.imag)+1.0))
        'lower bound on time between points from fraction x and fraction y on the interval'
        time = abs(self.x.time_begin-self.y.time_begin)-1.0
        
        
        if time == 0:
            'this happens if fractions are neighbors'
            time = 0.0000001
            
        'check if there could be any points with square-to-linear ratio exceeding specified lower bound'
        if pow(sq,2)/time < sq2l_lower_bound:
            return None
        
        'create sets of sub-fractions'
        x_set = self.x.next_step()
        y_set = self.y.next_step()
        
        fraction_pairs_list = list()
        for i in x_set:
            for j in y_set:
                fraction_pairs_list.append(fraction_pair(i,j))
                
        return fraction_pairs_list
            
    'calculate maximum square-to-linear ratio between all corners of the pair of fractions'
    def maximum_sq2l_ratio(self):
        'create list of corners for fraction x and fraction y'
        x_list = [arrow(self.x.coord_begin, self.x.time_begin)]
        y_list = [arrow(self.y.coord_begin, self.y.time_begin)]
        for x in self.x.bypass:
            x_list.append(arrow(x_list[-1].com + x.com, x_list[-1].time + x.time))
        for y in self.y.bypass:
            y_list.append(arrow(y_list[-1].com + y.com, y_list[-1].time + y.time))
        
        'iterate over all possible pairs'
        max_sq2l = [0.0]
        for i in x_list:
            for j in y_list:
                sq = pow(abs(i.com-j.com),2)
                time = abs(i.time-j.time)
                if time == 0:
                    continue
                sq2l = sq/time
                if sq2l > max_sq2l[0]:
                    max_sq2l = [sq2l,     #(float) maximal identified square-to-linear ratio
                                self.x.n, #(int) number of construction step
                                i.com,    #(complex) coordinate of the first point on the complex plane
                                i.time,   #(float) time (or linear coordinate) of the 1st point
                                j.com,    #(complex) coordinate of the 2nd point on the complex plane
                                j.time,   #(float) time (or linear coordinate) of the 2nd point
                                int(pow(len(self.x.dnplus1),self.n)),         #(int) the overall time in the interval
                                int(np.sqrt(pow(len(self.x.dnplus1),self.n))) #(int) the side of the constructed square
                                ]
                    
        return max_sq2l
