from GLC import GLC

P = {
        'S': 
            [
                ['A', 'b'], 
                ['A', 'B', 'c'],
            ],
        'B':
            [
                ['b', 'B'],
                ['A', 'd'],
                ['&']
            ],
        'A':
            [
                ['a', 'A'],
                ['&']
            ]
    }

glc = GLC(N=['S', 'B', 'A'], T=['b', 'c', 'a', 'd', '&'], S='S', P=P)
glc.setFollow()

# from GLC import GLC

# P = {
#         'S': 
#             [
#                 ['A', 'B', 'C'], 
#             ],
#         'A':
#             [
#                 ['a', 'A'],
#                 ['&']
#             ],
#         'B':
#             [
#                 ['b', 'B'],
#                 ['A', 'C', 'd']
#             ],
#         'C':
#             [
#                 ['c', 'C'],
#                 ['&']
#             ]
#     }

# glc = GLC(N=['S', 'A', 'B', 'C'], T=['b', 'c', 'a', 'd', '&'], S='S', P=P)
# glc.setFollow()