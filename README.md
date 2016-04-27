#Peanocode -- Processing Peano Curves in Python

Peanocode is a Python library for *encoding Peano curves*, *calculating square-to-linear ratio* and *searching for a minimal curve* based on the specified first step and fractal genius.

##Documentation

###Coding Peano curve
    The codes defining Peano curves introduced in 
        Bauman K., "One-side peano curves of fractal genus 9"
        Proceedings of the Steklov Institute of Mathematics 275 (1), 47-59

	In oreder to specify the curve user has to define 
	1) the order in which curve visits corners
	2) recurrent code of the next step based on the current one.
	
	By default, all curves start in the left lower corner. 
	The following code ["i","1","-i"] defines all curves starting in the left lower corner, then going up ("i"),
	then to the right ("1"), and, finally, down ("-i").
	
	Recurrenct code of the curve contains recurrent elements. The number of those elements is equal to the fractal genius of Peano Curve.
	
	Each recurrent element defines how to move, rotate or reflect the curve for consracting the
	corresponding fraction on the next step of Peano Curve construction.\s\s
	d - is original curve.
	s - represents reflecting the curve on the x-axis or conjucate on the complex plane
	o - represents reflecting the curve on the y-axis
	i - represents rotation or multiplying to i in the complex plane
	-i - represents rotation or multiplying to -i in the complex plane
	
####Examples:
	Peano - Hilbert curve\s\s
	d0=["i","1","-i"]\s\s
	dnplus1 = ["isd","d","d","-isd"]
	
	minimal N-curve from [Minimal Peano Curve][http://link.springer.com/article/10.1134/S0081543808040172]\s\s
	d0=["i","1-i","i"]\s\s
	dnplus1 = ["d","id","isd","sd","-isd","-id","d","id","isd"]\s\s
	
	minimal one side curve from [One-side peano curves of fractal genus 9][http://link.springer.com/article/10.1134/S0081543811080037]\s\s
	d0=["i","1","-i"]\s\s
	dnplus1 = ["d","isd","isod","-od","d","d","od","-isd","-isod"]
	


###Definition:
    **compute_sq_ratio(d0, dnplus1, C, N)** - is a function for calculating 
    the square-to-linear ratio for the specified Peano curve.
    
###Attributes:
    *d0*       			-  code of the basic step of the curve.\s\s
    *dnplus1*  			-  code for constructing the next step of the curve based on the current one. \s\s
    *sq2l_lower_bound*  -  a lower boundary on the square-to-linear ratio. It is used for reducing calculations. \s\s
    *N*        			-  Peano curve construction step number. The script constructs the specified Peano curve 
                		up to the N-th step and calculates square-to-linear ratios between all pairs of corners
                		on this step.
    
###Return:
    a list of variables describing the maximum square-to-linear ratio 
    and the example of pair of points reaching this maximum.
	
    [\s\s
        0: (float) maximum identified square-to-linear ratio\s\s
        1: (int) number of construction step\s\s
        2: (complex) coordinate of the first point on the complex plane\s\s
        3: (float) time (or linear coordinate) of the 1st point\s\s
        4: (complex) coordinate of the 2nd point on the complex plane\s\s
        5: (float) time (or linear coordinate) of the 2nd point\s\s
        6: (int) the overall time in the interval\s\s
        7: (int) the side of the constructed square\s\s
    ]
    
    ####Example:
        [6.0, 5, (8+16j), 490.66, (24+16j), 533.33, 1024, 32]






##Citing Peanocode

When [citing Peanocode in academic papers and theses][http://link.springer.com/article/10.1134/S0081543811080037], please use the following BibTeX entry:

@Article{Bauman2012,\s\s
		 author="Bauman, K. E.",\s\s
		 title="One-side peano curves of fractal genus 9",\s\s
		 journal="Proceedings of the Steklov Institute of Mathematics",\s\s
		 year="2012",\s\s
		 volume="275",\s\s
		 number="1",\s\s
		 pages="47--59",\s\s
		 abstract="This paper completes the analysis (begun by E.V. Shchepin and the author in 2008) of regular Peano curves of genus 9 in search of a curve with the minimum square-to-linear ratio. One-side regular Peano curves of genus 9 are considered, and, among these curves, a class of minimal curves with a square-to-linear ratio of 5 2/3 is singled out. A new language to describe curves is introduced which significantly simplifies the coding of these curves.",\s\s
		 issn="1531-8605",\s\s
		 doi="10.1134/S0081543811080037",\s\s
		 url="http://dx.doi.org/10.1134/S0081543811080037"\s\s
        }


Peano_code is open source software released under the [GNU LGPLv3 license][http://www.gnu.org/licenses/lgpl.html].\s\s
Copyright (c) 2016-now Konstantin Bauman