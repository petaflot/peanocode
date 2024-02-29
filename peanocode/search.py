from peanocode.compute_sq2l_ratio import compute_sq2l_ratio

''''
TODO:
     create function for clever search for a minimal curve 
     based on the given first step and fractal genius 
'''


# OLD - does not work
def search_o(d0,dnplus1,C,N):
    r = len(dnplus1)
    temp = dnplus1
    for i in range(pow(2,r)):
        t =[]
        u = i
        for j in range(r):
            s = u/pow(2,r-j-1)
            if s:
                temp[j] = temp[j].replace("o","").replace("d","od")
            else:
                temp[j] = temp[j].replace("o","")
            u -= s*pow(2,r-j-1)
        print(temp)
        print(compute_sq2l_ratio(d0,temp,C,N))
    
#search_o(d0,dnplus1,C,N)
