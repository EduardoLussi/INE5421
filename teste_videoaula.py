from GLC import GLC

P = {
        'E': 
            [
                ['E', '+', 'T'], 
                ['T']
            ],
        'T':
            [
                ['T', '*', 'F'],
                ['F']
            ],
        'F':
            [
                ['(', 'E', ')'],
                ['id']
            ]
    }

glc = GLC(N=['E', 'T', 'F'], T=['+', '*', '(', ')', 'id'], S='E', P=P)
print(glc.slrRecognizeSentence("id * id"))