# Copyright (C) 2016 Konstantin Bauman <kbauman@yandex.ru>
# Licensed under the GNU LGPL v3 - http://www.gnu.org/licenses/lgpl.html

import copy
import numpy as np
from peanocode.code import code
from peanocode.fraction import fraction, arrow

           
def conjugate_curve(curve):
    for arr in curve:
        arr.com = arr.com.conjugate()
        
def multiply_i_curve(curve):
    for arr in curve:
        arr.com = arr.com * complex(0,1)
        
def reflect_curve(curve, curve_type):
    curve.reverse()
    if curve_type == 0:
        for arr in curve:
            arr.com = arr.com.conjugate()
                        

'''
Class curve_step defines a curve on a certain construction step.
Attributes:
    curve    - internal code of the curve, i.e. list of arrows (see class arrow).
    n        - number of the construction step of the curve.
    d0       - internal code of the basic step of the curve. 
    dnplus1  - internal code for constructing the next step of the curve based on the current one. 
    type     - one-side (1) or diagonal (0) curve
'''
class curve_step:
    '''
    ["a","b","c"] is a list of times of visits of the 2nd, 3rd and 4th corner of the curve. 
    '''
    def __init__(self, d0, dnplus1, time = ["a","b","c"]):
        'create initial step'
        self.d0 = list()
        self.d0.append(arrow(complex(d0[0].replace("i","j")),time[0]))
        self.d0.append(arrow(complex(d0[1].replace("i","j")),time[1]))
        self.d0.append(arrow(complex(d0[2].replace("i","j")),time[2]))
        'create curve'
        self.curve = copy.deepcopy(self.d0)
        'encode dnplus1 from user input to internal code'
        self.encode_dnplus1(dnplus1)
        'get type of the curve: one-side/diagonal'
        self.get_type(d0)
        'initiate step number'
        self.n = 0
    
    '''
    get type of the curve from the initial step (d0)
    type = 1 - one-side curve
    type = 0 - diagonal curve 
    '''
    def get_type(self, d0):
        second_step = complex(d0[1].replace("i","j"))
        self.type = 0 if second_step == 1 else 1
        
    'encode dnplus1 from user input to internal class code'
    def encode_dnplus1(self,dnplus1):
        self.dnplus1 = list()
        for frac in dnplus1:
            o = 1 if "o" in frac else 0
            s = 1 if "s" in frac else 0
            m = -1 if "-" in frac else 1
            if "i" in frac:
                self.dnplus1.append(code(complex(0,m),s,o))
            else:
                self.dnplus1.append(code(complex(m,0),s,o))
    
    'calculate the number of arrows in the curve'
    def len(self):
        return len(self.curve)
    
    'calculate the length of the side of the square'
    def side(self):
        return int(np.sqrt(self.len()/3)+1)
    
    
    '''
    Create next step of the curve based on the current one
    and the code for constructing the next step.
    '''
    def make_next(self):
        next_step_curve = list()
        for transformation_code in self.dnplus1:
            'create new fraction'
            temp_curve = copy.deepcopy(self.curve)
            'apply transformations'
            if transformation_code.if_reflection:
                reflect_curve(temp_curve, self.type)
            if transformation_code.if_conjugate:
                conjugate_curve(temp_curve)
            i = copy.copy(transformation_code.complex)
            while i != 1:
                multiply_i_curve(temp_curve)
                i /= 1j
            next_step_curve += copy.deepcopy(temp_curve)
        'assign next step of the curve to the class'
        self.curve = next_step_curve
        self.n += 1

    '''
    Check if the code specifies valid curve and
    Fills the times between corners with the exact values
    '''
    def curve_validation(self):
        side = self.side()
        visited_corner_number = 0
        time_list = {}
        b_corners = [complex(0,(side-1)),complex((side-1),0),complex((side-1),(side-1))]
        'initialize values for corner times'
        time = {"a":0.,"b":0.,"c":0.}
        
        '''
        compute number of times which curve visits each corner (vertex)
        of each pattern on the current step
        '''
        corners = dict()
        for i in range(side):
            for j in range(side):
                'fill corners with zeros'
                corners[complex(i,j)] = 0
                
        'identify starting point in the left lower corner'
        current_point = (0+0j)
        if  current_point in corners:
            corners[current_point]+=1
        else:
            return -1
        
        'follow the curve and fill in corners dictionary'
        for step in self.curve:
            current_point += step.com
            time[step.time] += 1
            
            'if the curve reaches next corner of the original square we update time information'
            if current_point in b_corners:
                time_list[visited_corner_number] = time.copy()
                time = {"a":0.,"b":0.,"c":0.}
                visited_corner_number += 1
            
            'try to increase number of visits to the corner (vertex)'  
            if  current_point in corners:
                corners[current_point] += 1
            else:
                'curve went out from the initial square'
                return -1
        
        'check if curve visited all corners'
        if 0 in corners.values():
            return 0
        'check if curve finished in the right corner of the initial square'
        if self.type == 0:
            if current_point != side - 1:
                return -2
        else:
            if current_point != complex(side-1, side-1):
                return -2
        
        '''
        Calculate time needed to reach 2nd, 3rd and 4th corner (a,b,c)
        '''
        num = self.len()/3
        b = np.matrix([[1,1,1],
                       [float(time_list[0]["a"]-num),float(time_list[0]["b"]),    float(time_list[0]["c"])],
                       [float(time_list[1]["a"]),    float(time_list[1]["b"]-num),float(time_list[1]["c"])]])
        c = np.matrix([[1],[0.],[0.]])
        e = (b.I*c).T
        
        'fill the curve with the exact time values'
        for arr in self.curve:
            if arr.time == "a":
                arr.time = float(e[0,0])
            if arr.time == "b":
                arr.time = float(e[0,1])
            if arr.time == "c":
                arr.time = float(e[0,2])
        
        for arr in self.d0:
            if arr.time == "a":
                arr.time = float(e[0,0])
            if arr.time == "b":
                arr.time = float(e[0,1])
            if arr.time == "c":
                arr.time = float(e[0,2])
        
        'curve is valid'
        return 1
    
    
    '''
    create set of fractions, i.e. squares (see class fraction)
    '''
    def make_fractions_set(self):
#         l = math.sqrt(len(self.dnplus1))
        sq_list = list()
        
        temp_arrow_list = list()
        temp_sq_start_cordinates = 0+0j
        current_coordinates = temp_sq_start_cordinates
        temp_sq_left_lower_cordinates = current_coordinates
        temp_time = 0.0
        
        '''
        follow the curve and create a set of fractions, i.e. squares (see class fraction)
        '''
        i = 0 #counter for catching fractions of each three arrows
        for arrow in self.curve:
            temp_arrow_list.append(arrow)
            current_coordinates += arrow.com 
            if current_coordinates.real < temp_sq_left_lower_cordinates.real:
                temp_sq_left_lower_cordinates = complex(current_coordinates.real, temp_sq_left_lower_cordinates.imag)
            if current_coordinates.imag < temp_sq_left_lower_cordinates.imag:
                temp_sq_left_lower_cordinates = complex(temp_sq_left_lower_cordinates.real, current_coordinates.imag)
            i+=1
            if i%3 == 0:
                'each fraction consists of 3 arrows. We catch them and create squares.'
                sq_list.append(fraction(temp_arrow_list, self.d0, self.dnplus1, self.type, self.dnplus1[int(i/3)-1]))
                sq_list[-1].n = self.n
                sq_list[-1].coord_begin = temp_sq_start_cordinates
                temp_sq_start_cordinates = current_coordinates 
                sq_list[-1].left_lower_cordinates = temp_sq_left_lower_cordinates
                temp_sq_left_lower_cordinates = current_coordinates
                sq_list[-1].time_begin = temp_time
                temp_time += 1.0
                temp_arrow_list = list()
        return sq_list
