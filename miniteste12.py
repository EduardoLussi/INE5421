
from GLC import GLC

productions = {
    "E" : [['T', "E'"]],
    "E'" : [['∨', 'T', "E'"], ['&']],
    "T" : [['F', "T'"]],
    "T'" : [['∧', 'F', "T'"] , ['&']],
    "F" : [['¬', 'F'], ['id']],
}


glc = GLC(N=['E', "E'", "T", "T'", 'F'], T=['∨', '∧', 'id', '¬', '&'], S='E', P=productions)
print(glc)
glc.setFirst()
glc.setFollow()
glc.llRecognizeSentence(["id", "∨", "id", "∧", "id"])
