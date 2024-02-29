# Copyright (C) 2016 Konstantin Bauman <kbauman@yandex.ru>
# Licensed under the GNU LGPL v3 - http://www.gnu.org/licenses/lgpl.html

import sys
#sys.path.append('../')
#sys.path.append('../../')
import logging
from peanocode.compute_sq2l_ratio import compute_sq2l_ratio




def compute_square_to_linear_ratio(d0,dnplus1,N,sq2l_lower_bound,logger,name='Peano Curve'):
    result = compute_sq2l_ratio(d0,dnplus1,N,sq2l_lower_bound,logger)
    if len(result) > 1:
        logger.info('\n\n%s\nSquare-to-linear ratio = %.4f'%(name,result[0])+
                    '\nStep = %d, Overall time = %d, Side of square = %d'%(result[1],result[6],result[7])+
                    '\nPoints [%.3f,%s],\t[%.3f,%s]\n'%(result[3],str(result[2]),result[5],str(result[4])))
    else:
        logger.error('Program did not find any maximums on the step %d exceeding %f'%(N,sq2l_lower_bound))



if __name__ == '__main__':
    logger = logging.getLogger('peano_code')
    logging.basicConfig(format='%(asctime)s : %(name)-12s: %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.DEBUG)
    logger.info("running %s" % ' '.join(sys.argv))
    
    
    '''PARAMETERS'''
    N = 7  #step number
    sq2l_lower_bound = 5.5 #lower constant


    name = 'Peano-Gilbert'    
    d0=["i","1","-i"]
    dnplus1 = ["isd","d","d","-isd"]
    compute_square_to_linear_ratio(d0,dnplus1,N,sq2l_lower_bound,logger,name)
    
    
#     N = 4  #step number
#     sq2l_lower_bound = 5.5 #lower constant
    name = 'minimal N-curve'
    d0=["i","1-i","i"]
    dnplus1 = ["d","id","isd","sd","-isd","-id","d","id","isd"]
    compute_square_to_linear_ratio(d0,dnplus1,N,sq2l_lower_bound,logger,name)
    
#     N = 4  #step number
#     sq2l_lower_bound = 5.5 #lower constant
    name = 'minimal one side curve'
    d0=["i","1","-i"]
    dnplus1 = ["d","isd","isod","-od","d","d","od","-isd","-isod"]
    compute_square_to_linear_ratio(d0,dnplus1,N,sq2l_lower_bound,logger,name)
    
