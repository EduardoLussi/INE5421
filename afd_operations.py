from AF import AF
from itertools import product


def cartesian_product(af1: AF, af2: AF) -> AF:
    """ 
    Calcula o produto cartesiano de dois autômatos finitos.
    Método auxiliar para os algoritmos de construção da união e interseção 
    de AFDs por produto cartesiano (Sipser, 1.25).
    Presume-se que os AFs de entrada (af1 e af2) sejam determinísticos.
    """

    # Atualiza nomes de estados, para garantir que não haverão estados com nomes repetidos
    if len(set(af1.K).intersection(set(af2.K))) > 0:
        common_names = True
        af1_K = [state + '_1' for state in af1.K]
        af2_K = [state + '_2' for state in af2.K]
        af1_F = [state + '_1' for state in af1.F]
        af2_F = [state + '_2' for state in af2.F]
    else:
        common_names = False
        af1_K = af1.K
        af2_K = af2.K
        af1_F = af1.F
        af2_F = af2.F

    # Estado inicial
    s = (af1.s + '_1', af2.s + '_2') if common_names else (af1.s, af2.s)

    # Cria conjunto de valores de entrada
    sigma = set()
    for i in af1.sigma + af2.sigma:
        sigma.add(i)

    # Gera estados possíveis de serem usados
    union_k = list(product(af1_K, af2_K))

    # Define transições
    delta = []
    for q1, q2 in union_k:
        if common_names:
            q1, q2 = q1[:-2], q2[:-2]
        for symbol in sigma:
            try:
                t1 = af1.getTransition(q1, symbol)
                t2 = af2.getTransition(q2, symbol)
                # se len > 1, o autômato não é determinístico; se
                assert(len(t1) <= 1 and len(t2) <= 1)
            except AssertionError:
                print("Ao menos um FA de entrada não era determinístico.")
                print("Use algoritmo de determinização antes de continuar :)")
            except IndexError:
                '''
                Este erro pode indicar um dos seguintes casos:
                - os AFDs não possuem todas as transições explícitas; ou
                - os AFDs não compartilham todos os símbolos de entrada.
                Em ambos os casos, o algoritmo deve funcionar.
                '''
                continue
            transition = (t1[0] + '_1', t2[0] +
                          '_2') if common_names else (t1[0], t2[0])
            delta.append(((q1, q2), symbol, transition))
    af_prod = AF(union_k, sigma, delta, s)
    return af1_F, af2_F, af1_K, af2_K, af_prod


def format_product(af: AF):
    """Formatador para tuplas usadas no produto cartesiano"""
    def merge_tuples(x): return '{' + f'{x[0]},{x[1]}' + '}'
    af.K = list(map(merge_tuples, af.K))
    af.F = list(map(merge_tuples, af.F))
    af.s = merge_tuples(af.s)
    delta = list(zip(*af.delta))
    delta[0] = list(map(merge_tuples, delta[0]))
    delta[2] = list(map(merge_tuples, delta[2]))
    af.delta = list(zip(*delta))


def union(af1: AF, af2: AF) -> AF:
    """Utiliza o produto cartesiano para gerar a união de dois AFDs"""
    af1_F, af2_F, af1_K, af2_K, af_prod = cartesian_product(af1, af2)
    final_union = list(set(product(af1_F, af2_K)) | set(product(af1_K, af2_F)))
    af_prod.F = final_union
    # Remove estados inalcançáveis
    ...
    format_product(af_prod)
    return af_prod


def intersection(af1: AF, af2: AF) -> AF:
    """Utiliza o produto cartesiano para gerar a interseção de dois AFDs"""
    af1_F, af2_F, af1_K, af2_K, af_prod = cartesian_product(af1, af2)
    final_intersection = list(product(af1_F, af2_F))
    af_prod.F = final_intersection
    # Remove estados inalcançáveis
    ...
    format_product(af_prod)
    return af_prod
