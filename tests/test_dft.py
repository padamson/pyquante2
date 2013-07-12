import unittest
import numpy as np
from pyquante2.dft.functionals import xs,cvwn,xb88
from pyquante2.dft.reference import data

def amax(x): return np.amax(np.absolute(x))

class test_dft(unittest.TestCase):
    def test_xs(self):
        na = data['xs'][:,0]
        nb = data['xs'][:,1]
        fa,dfa = xs(na)
        fb,dfb = xs(nb)
        max_f = amax(fa+fb-data['xs'][:,5])
        max_dfa = amax(dfa-data['xs'][:,6])
        max_dfb = amax(dfb-data['xs'][:,7])
        #print np.column_stack([na,nb,data['xs'][:,5]-fa-fb])
        self.assertAlmostEqual(max_f,0,5) ## Fix this!
        self.assertAlmostEqual(max_dfa,0)
        self.assertAlmostEqual(max_dfb,0)

    @unittest.skip("Skipping CVWN since it doesn't work")
    def test_cvwn(self):
        na = data['cvwn'][:,0]
        nb = data['cvwn'][:,1]
        f,dfa,dfb = cvwn(na,nb)
        max_f = amax(f-data['cvwn'][:,5])
        max_dfa = amax(dfa-data['cvwn'][:,6])
        max_dfb = amax(dfb-data['cvwn'][:,7])
        #print np.column_stack([na,nb,data['cvwn'][:,7],dfb])
        self.assertAlmostEqual(max_f,0)
        self.assertAlmostEqual(max_dfa,0)
        self.assertAlmostEqual(max_dfb,0)

    def test_xb88(self):
        na = data['xb88'][:,0]
        nb = data['xb88'][:,1]
        gaa = data['xb88'][:,2]
        gbb = data['xb88'][:,4]
        fa,dfa,dfga = xb88(na,gaa)
        fb,dfb,dfgb = xb88(nb,gbb)
        max_f = amax(fa+fb-data['xb88'][:,5])
        max_dfa = amax(dfa-data['xb88'][:,6])
        max_dfb = amax(dfb-data['xb88'][:,7])
        #print np.column_stack([na,nb,data['xb88'][:,5]-fa-fb])
        self.assertAlmostEqual(max_f,0,5)
        self.assertAlmostEqual(max_dfa,0)
        self.assertAlmostEqual(max_dfb,0)

def runsuite(verbose=True):
    if verbose: verbosity=2
    else: verbosity=1
    suite = unittest.TestLoader().loadTestsFromTestCase(test_dft)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return

def debugsuite():
    import cProfile,pstats
    cProfile.run('runsuite()','prof')
    prof = pstats.Stats('prof')
    prof.strip_dirs().sort_stats('time').print_stats(15)

if __name__ == '__main__':
    import sys
    if "-d" in sys.argv:
        debugsuite()
    else:
        runsuite()
    
    
        
