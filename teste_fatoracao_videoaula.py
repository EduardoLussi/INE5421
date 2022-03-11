from GLC import GLC

P = {
    'S': [list('AC'), list('BC')],
    'A': [list('aD'), list('cC')],
    'B': [list('aB'), list('dD')],
    'C': [list('eC'), list('eA')],
    'D': [list('fD'), list('CB')],
}

glc = GLC(N=list("SABCD"), T=list('abcdef'), S='S', P=P, name='first grammar')
print(glc)
glc.left_factoring(iters=1)
print(glc)