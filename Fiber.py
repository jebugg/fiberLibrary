"""
Author: Jens Buvik Bugge
"""

class FiberTypes:
    def __init__(self, name:str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

class Fiber:
    def __init__(self, id:int, name:str, *, tensileModulus:float, tensileStrength:float, density:float, ft:FiberTypes, comment="") -> None:
        self._id = id
        self._name = name
        self._E1 = tensileModulus
        self._strength = tensileStrength
        self._rho = density
        self._type = ft
        self.comment = comment

    @property
    def datastructure(self):
        return [{"name":"id", "datatype":int},
                {"name":"name","datatype":str},
                {"name":"E1","datatype":float},
                {"name":"strength","datatype":float},
                {"name":"density","datatype":float},
                {"name":"fibertype","datatype":Fiber.FiberTypes},
                {"name":"comment","datatype":str}
            ]

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, nn):
        if nn != self._name:
            self._name = nn
        return None
    
    @property
    def dictFormat(self):
        return {"id":self._id, 
                "type":self._type, 
                "name":self._name, 
                "modulus":self._E1, 
                "UTS":self._strength, 
                "rho":self._rho, 
                "comment":self.comment
            }

    @property
    def astuple(self):
        return (self._id, 
                self._name, 
                self._E1, 
                self._strength, 
                self._rho, 
                self._type, 
                self.comment
            )

    def test(self):
        print(f"""### {self._name} data: ### \nid:    {self._id} \nE-mod: {self._E1} \nUTS:   {self._strength} \nrho:   {self._rho} \ntype:  {self._type.name} \ncomments: {self.comment}\n""")
        return None

### TESTCODE ###
def getTestFibers(numFibers:int = 1) -> list[Fiber]:
    from testing import getRandFloat, getRandInt
    fiberTypes = [FiberTypes("Carbon"),FiberTypes("Aramid"), FiberTypes("Glass")]
    names = ["YSH60A", "MR70", "T1100", "YSH65A", "T700", "T300", "T800", "HS40", "HS80"]
    fibers = []
    for i in range(numFibers):
        name = names[getRandInt(0, len(names)-1)]
        fibers.append(Fiber(i, name, 
                      tensileModulus=getRandInt(), 
                      tensileStrength=getRandFloat(2,6), 
                      density=getRandFloat(0.1e-09, 1e-09), 
                      ft=getRandInt(0, len(fiberTypes)-1), 
                      comment="Testfiber"))
    return fibers

if __name__ == "__main__":
    fibers = getTestFibers(4)
    for fiber in fibers:
        fiber.test()

