#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  PyFiVol - Python-based finite volume PDE solver
 # 
 #  FILE: "sourceVariable.py"
 #                                    created: 11/12/03 {10:39:23 AM} 
 #                                last update: 1/16/04 {11:59:24 AM}
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-12 JEG 1.0 original
 # ###################################################################
 ##

import Numeric

from fivol.variables.cellVariable import CellVariable
from fivol.examples.phase.phase.toolsTmp import addOverFaces

class SourceVariable(CellVariable):

    def __init__(self,
                 phase = None,
                 theta = None,
                 diffCoeff = None,
                 halfAngleVariable = None,
                 parameters = None):

        CellVariable.__init__(self, theta.getMesh())

        self.parameters = parameters
        self.phase = self.requires(phase)
        self.theta = self.requires(theta)
        self.diffCoeff = self.requires(diffCoeff)
        self.halfAngleVariable = self.requires(halfAngleVariable)

    def calcValue(self):

        mesh = self.theta.getMesh()
        c2 = self.parameters['anisotropy']
        
        thetaGradDiff = self.theta.getFaceGrad()[:] - self.theta.getFaceGradNoMod()[:]

        correctionTerm = addOverFaces(faceGradient = thetaGradDiff,
                                      faceVariable = self.diffCoeff[:],
                                      mesh = mesh,
                                      NCells = len(self.phase[:]))

        halfAngleSq = self.halfAngleVariable[:] * self.halfAngleVariable[:]
        beta = (1. - halfAngleSq) / (1. + halfAngleSq)
        dbeta = self.parameters['symmetry'] * 2. * self.halfAngleVariable[:] / (1. + halfAngleSq)

        self.value = correctionTerm + self.parameters['alpha']**2 * c2 * dbeta * self.phase.getGrad().getMag()[:] * (1. + c2 * beta)
        
    

