from GLC import GLC

P = {
        'S': 
            [
                ['S', 'or', 'A'], 
                ['A']
            ],
        'A':
            [
                ['A', 'and', 'B'],
                ['B']
            ],
        'B':
            [
                ['not', 'B'],
                ['(', 'S', ')'],
                ['true'],
                ['false']
            ]
    }

glc = GLC(N=['S', 'A', 'B'], T=['or', 'and', '(', ')', 'not', 'true', 'false'], S='S', P=P)
print(glc.slrRecognizeSentence("not ( false )"))