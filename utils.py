import numpy as np

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class orbitalElements:
    def __init__(self, r, v, mu):
        I = np.array([1, 0, 0])
        J = np.array([0, 1, 0])
        K = np.array([0, 0, 1])

        self.r = r
        self.v = v
        self.mu = mu

        self._calculateVectors()
        self._calculateOrbitalElements()

    def _calculateVectors(self):
        self.h = np.cross(self.r, self.v)
        self.n = np.cross(K, self.h)
        self.e = 1/self.mu * ((np.linalg.norm(self.v)**2 - self.mu/np.linalg.norm(self.r))*self.r - np.dot(self.r, self.v)*self.v)

    def _calculateOrbitalElements(self):
        self.p = np.linalg.norm(self.h)**2/self.mu
        self.i = np.arccos(self.h[2]/np.linalg.norm(self.h))
        self.Omega = np.arccos(self.n[2]/np.linalg.norm(self.n))
        self.omega = np.arccos(np.dot(self.n, self.e)/(np.linalg.norm(self.n)*np.linalg.norm(self.e)))

    def toCartesian(self):
        pass
