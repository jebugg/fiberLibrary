"""
Author: Jens Buvik Bugge
"""
from Fiber import Fiber

class FabricType:
    def __init__(self, name:str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

class UseCase:
    def __init__(self, name:str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class Lamina:
    def __init__(self, id:int, name:str, fiber:Fiber, fabricType:FabricType, useCase:UseCase, *, faw:float, thickness:float, E1:float = None, E2:float = None, G12:float = None, nu:float = None, rho:float = None, comment:str = "") -> None:
        self._id = id
        self._name = name
        self._fiber = fiber
        self._type = fabricType
        self._use = useCase
        self._E1 = E1
        self._E2 = E2
        self._G12 = G12
        self._nu = nu
        self._rho = rho
        self._faw = faw
        self._t = thickness
        self.comment = comment

    @property
    def thickness(self):
        return self._t

    @property
    def data(self):
        return {"E1":self._E1, "E2":self._E2, "G12":self._G12, "nu":self._nu}
    
    @property
    def dictFormat(self):
        return {"id": self._id, 
                "name": self._name,
                "fiber": self._fiber,
                "use": self._use,
                "e1": self._E1,
                "e2": self._E2,
                "g12": self._G12,
                "nu": self._nu,
                "rho": self._rho,
                "faw": self._faw,
                "thickness": self._t,
                "comment": self.comment
            }

    @property
    def info(self):
        return {"id":self._id, "name:":self._name, "FAW":self._faw, "usecase":self._use}