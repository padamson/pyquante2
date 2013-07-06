"""
Class to create an atom object

>>> h = atom(1,0,0,0)
>>> h
1 H     0.000000     0.000000     0.000000
>>> h.r
array([ 0.,  0.,  0.])

 Copyright (c) 2004, Richard P. Muller. All Rights Reserved. 

 PyQuante version 2.0 and later is covered by the GPL
 license. Please see the file LICENSE that is part of this
 distribution. 
"""
import numpy as np
from pyquante2.geo.elements import color,radius
from pyquante2.constants import ang2bohr
from pyquante2.utils import norm2

class atom:
    def __init__(self,atno,x,y,z,**kwargs):
        self.atno = atno
        self.r = np.array([x,y,z],'d')
        self.units = kwargs.get('units','bohr').lower()
        assert self.units[:4] in ['bohr','angs']
        if not self.units == 'bohr':
            self.r *= ang2bohr
        return

    def atuple(self): return (self.atno,self.r[0],self.r[1],self.r[2])
    def nsxyz(self):
        from pyquante2.geo.elements import symbol
        return (self.atno,symbol[self.atno],self.r[0],self.r[1],self.r[2])
    def __repr__(self): return "%d %s %12.6f %12.6f %12.6f" % self.nsxyz()
    def __getitem__(self, i): return self.r[i]

    def xyz(self):
        from pyquante2.geo.elements import symbol
        return "%4s %12.6f %12.6f %12.6f" % (symbol[self.atno],self.r[0],self.r[1],self.r[2])

    def distance(self,other): return np.sqrt(norm2(self.r-other.r))
    def color(self): return color[self.atno]
    def radius(self): return radius[self.atno]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
