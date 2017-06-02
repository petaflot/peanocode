# Peanocode -- Processing Peano Curves in Python

Peanocode is a Python library for *encoding Peano curves*, *calculating square-to-linear ratio* and *searching for a minimal curve* based on the specified first step and fractal genius.

## Documentation

### Coding Peano curve

The codes defining Peano curves introduced in <br>
Bauman K., "One-side peano curves of fractal genus 9" <br>
Proceedings of the Steklov Institute of Mathematics 275 (1), 47-59

In oreder to specify the curve user has to define 
- 1) the order in which curve visits corners
- 2) recurrent code of the next step based on the current one.
	
By default, all curves start in the left lower corner. 
The following code ["i","1","-i"] defines all curves starting in the left lower corner, then going up ("i"),
then to the right ("1"), and, finally, down ("-i").
	
Recurrenct code of the curve contains recurrent elements. The number of those elements is equal to the fractal genius of Peano Curve.
	
Each recurrent element defines how to move, rotate or reflect the curve for consracting the
corresponding fraction on the next step of Peano Curve construction.

	d - is original curve.
	s - represents reflecting the curve on the x-axis or conjucate on the complex plane
	o - represents reflecting the curve on the y-axis
	i - represents rotation or multiplying to i in the complex plane
	-i - represents rotation or multiplying to -i in the complex plane
	
#### Examples:

Peano - Hilbert curve<br>
![Hilbert curve](https://spacefillingcurves.files.wordpress.com/2015/03/hilbert-1-to-4-600px.png)

	d0 	= ["i","1","-i"]
	dnplus1 = ["isd","d","d","-isd"]
	
Minimal N-curve from [Minimal Peano Curve](http://link.springer.com/article/10.1134/S0081543808040172)

	d0 	= ["i","1-i","i"]
	dnplus1 = ["d","id","isd","sd","-isd","-id","d","id","isd"]
	
minimal one side curve from [One-side peano curves of fractal genus 9](http://link.springer.com/article/10.1134/S0081543811080037)

	d0 	= ["i","1","-i"]
	dnplus1 = ["d","isd","isod","-od","d","d","od","-isd","-isod"]
	


### Calculatin square-to-linear ratio:

**compute_sq_ratio**(d0, dnplus1, C, N) - is a function for calculating 
the square-to-linear ratio for the specified Peano curve.
    
### Attributes:

    d0       			-  code of the basic step of the curve.
    dnplus1  			-  code for constructing the next step of the curve based on the current one. 
    sq2l_lower_boun		-  a lower boundary on the square-to-linear ratio. It is used for reducing calculations. 
    N        			-  Peano curve construction step number. The script constructs the specified Peano curve 
                		up to the N-th step and calculates square-to-linear ratios between all pairs of corners
                		on this step.
    
### Return:
List of variables describing the maximum square-to-linear ratio 
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
    
#### Example:
 
     [6.0, 5, (8+16j), 490.66, (24+16j), 533.33, 1024, 32]

### Where to start
Run run/compute_sq2l_ratio_examples.py

	python compute_sq2l_ratio_examples.py
	2016-04-28 00:07:25,411 : peano_code  : INFO : running compute_sq2l_ratio_examples.py
	2016-04-28 00:07:25,575 : peano_code  : INFO :
	
	Peano-Gilbert
	Square-to-linear ratio = 6.0000
	Step = 7, Overall time = 16384, Side of square = 128
	Points [7850.667,(32+64j)],	[8533.333,(96+64j)]
	
	2016-04-28 00:07:56,062 : peano_code  : INFO :
	
	minimal N-curve
	Square-to-linear ratio = 5.6667
	Step = 7, Overall time = 4782969, Side of square = 2187
	Points [1048119.750,1215j],	[1087485.750,(243+1620j)]
	
	2016-04-28 00:08:01,949 : peano_code  : INFO :
	
	minimal one side curve
	Square-to-linear ratio = 5.6667
	Step = 7, Overall time = 4782969, Side of square = 2187
	Points [2391484.500,2187j],	[2745778.500,(1215+1458j)]

### ToDo

- create function for clever search for a minimal curve 
  based on the given first step and fractal genius 




## Citing Peanocode

When [citing Peanocode in academic papers and theses](http://link.springer.com/article/10.1134/S0081543811080037), please use the following BibTeX entry:

@Article{Bauman2012,<br>
		 author="Bauman, K. E.",<br>
		 title="One-side peano curves of fractal genus 9",<br>
		 journal="Proceedings of the Steklov Institute of Mathematics",<br>
		 year="2012",<br>
		 volume="275",<br>
		 number="1",<br>
		 pages="47--59",<br>
		 abstract="This paper completes the analysis (begun by E.V. Shchepin and the author in 2008) of regular Peano curves of genus 9 in search of a curve with the minimum square-to-linear ratio. One-side regular Peano curves of genus 9 are considered, and, among these curves, a class of minimal curves with a square-to-linear ratio of 5 2/3 is singled out. A new language to describe curves is introduced which significantly simplifies the coding of these curves.",<br>
		 issn="1531-8605",<br>
		 doi="10.1134/S0081543811080037",<br>
		 url="http://dx.doi.org/10.1134/S0081543811080037"<br>
        }


Peanocode is open source software released under the [GNU LGPLv3 license](http://www.gnu.org/licenses/lgpl.html).<br>
Copyright (c) 2016-now Konstantin Bauman
