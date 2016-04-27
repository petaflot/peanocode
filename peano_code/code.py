# Copyright (C) 2016 Konstantin Bauman <kbauman@yandex.ru>
# Licensed under the GNU LGPL v3 - http://www.gnu.org/licenses/lgpl.html

'''
class for coding fractions of Peano curve
'''
class code:
    def __init__(self, complex_coordinates, if_conjugate, if_reflection):
        self.complex = complex_coordinates
        self.if_conjugate = if_conjugate
        self.if_reflection = if_reflection
    
    def copy_code(self):
        return code(self.complex,self.if_conjugate,self.if_reflection)
    
    def print_code(self):
        print (self.complex,self.if_conjugate,self.if_reflection)
        
def get_next_code(prev_code, n_code):
    c = n_code.complex
    if_conjugate = n_code.if_conjugate    
    if_reflection = n_code.if_reflection
    if prev_code.if_reflection == 1:
        c = c.conjugate()
        if_reflection += 1
    if prev_code.if_conjugate == 1:
        c = c.conjugate()
        if_conjugate += 1  
    c *= prev_code.complex
    return code(c,if_conjugate%2,if_reflection%2)