class Fiber:
    def __init__(self, id, name, E1, E2, G12, nu, rho, ft="Carbon", comment=""):
        self._id = id
        self._name = name
        self._E1 = E1
        self._E2 = E2
        self._G12 = G12
        self._nu = nu
        self._rho = rho
        self._type = ft
        self._comment = comment

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, nn):
        if nn != self._name:
            self._name = nn
        