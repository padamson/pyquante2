"""
Create a molecule for use in pyquante
>>> h = molecule([(1,0,0,0)])
>>> h
[(1, 0.0, 0.0, 0.0)]

 Copyright (c) 2004, Richard P. Muller. All Rights Reserved. 

 PyQuante version 2.0 and later is covered by the GPL
 license. Please see the file LICENSE that is part of this
 distribution. 
"""
import numpy as np
from pyquante2 import settings
from pyquante2.geo.atom import atom
from pyquante2.utils import upairs,norm2

class molecule:
    """
    >>> from pyquante2.geo.samples import h2
    >>> round(h2.nuclear_repulsion(), 6)
    0.72236
    >>> h2.nel()
    2
    >>> h2.nocc()
    1
    """
    def __init__(self,atomlist=[],**kwargs):
        self.atoms = []
        self.charge = int(kwargs.get('charge',settings.molecular_charge))
        self.multiplicity = int(kwargs.get('multiplicity',settings.spin_multiplicity))
        self.name = kwargs.get('name','pyquante2 molecule')

        self.units = kwargs.get('units',settings.units).lower()

        if atomlist:
            for atuple in atomlist:
                self.atoms.append(atom(*atuple,units=self.units))
        return

    def __repr__(self): return repr(self.atoms)
    def __getitem__(self,i): return self.atoms.__getitem__(i)

    def _repr_html_(self,tablehead=False):
        import xml.etree.ElementTree as ET
        top = ET.Element("html")
        h2 = ET.SubElement(top,"h2")
        h2.text = self.name
        p = ET.SubElement(top,"p")
        p.text = "Charge = %d, Multiplicity = %d" % (self.charge,self.multiplicity)
        table = ET.SubElement(top,"table")
        if tablehead:
            tr = ET.SubElement(table,"tr")
            for item in ["#","Atno","Symbol","x","y","z"]:
                th = ET.SubElement(tr,"th")
                th.text = item
        for i,atom in enumerate(self.atoms):
            tr = ET.SubElement(table,"tr")
            td = ET.SubElement(tr,"td")
            td.text = str(i)
            n,s,x,y,z = atom.nsxyz()
            td = ET.SubElement(tr,"td")
            td.text = str(n)
            td = ET.SubElement(tr,"td")
            td.text = s
            td = ET.SubElement(tr,"td")
            td.text = "%.5f" % x
            td = ET.SubElement(tr,"td")
            td.text = "%.5f" % y
            td = ET.SubElement(tr,"td")
            td.text = "%.5f" % y
        return ET.tostring(top)

    def nuclear_repulsion(self):
        return sum(ati.atno*atj.atno/np.sqrt(norm2(ati.r-atj.r)) for ati,atj in upairs(self))

    def nel(self):
        "Number of electrons of the molecule"
        return sum(atom.atno for atom in self) - self.charge
    
    def nocc(self): return sum(divmod(self.nel(),2))
    def nclosed(self): return self.nel()//2
    def nopen(self): return divmod(self.nel(),2)[1]
    def nup(self): return self.nocc()
    def ndown(self): return self.nclosed()

    def xyz(self,title=None,fobj=None):
        """
        Output molecule in [xyz format](http://en.wikipedia.org/wiki/XYZ_file_format).
        """
        if title is None:
            title = self.name
        lines = ["%d" % len(self.atoms),"%s" % title]
        for atom in self.atoms:
            lines.append(atom.xyz())
        record = "\n".join(lines)
        if fobj:
            fobj.write(record)
        else:
            print record
        return

    def pyquante1(self,name="pyq2 molecule"):
        """
        Make a PyQuante1 Molecule object that can be passed into that program for
        testing/debugging purposes.
        """
        from PyQuante import Molecule
        atuples = [(a.atno,tuple(a.r)) for a in self.atoms]
        return Molecule(name,atuples,charge=self.charge,multiplicity=self.multiplicity)
                 
        
        


if __name__ == '__main__':
    import doctest
    doctest.testmod()
