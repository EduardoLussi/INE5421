import copy

from AF import AF
from afd_operations import union, intersection
from GLC import GLC

AFs = []    # Lista de autômatos
Grammars = []   # Lista de gramáticas

while True: # Loop principal do programa
    print(f"\n------------ MENU PRINCIPAL ------------\n")

    print("1-  Importar autômato")
    print("2-  Visualizar autômato")
    print("3-  Exportar autômato")
    print("4-  Remover autômato")
    print("5-  Determinizar autômato")
    print("6-  Reconhecer sentença")
    print("7-  Minimizar autômato")
    print("8-  Unir autômatos")
    print("9-  Interseccionar autômatos")
    print("10- Converter ER para AFD")
    print("11- Importar gramática")
    print("12- Visualizar gramática")
    print("13- Exportar gramática")
    print("14- Remover gramática")
    print("15- Eliminação de recursão à esquerda")
    print("16- Fatoração")
    print("17- Reconhecer sentença via tabela preditivo LL(1)")
    print("18- Reconhecer sentença via SLR(1)")
    print("19- Sair")

    op = int(input("\nDigite uma opção: "))

    if op == 1:
        print(f"\n----------- IMPORTAR AUTÔMATO ----------\n")

        name = input("Nome do novo autômato: ")
        file = input("Nome do arquivo: ")

        af = AF(name=name)

        try:
            af.readData(f"testes/{file}")
        except:
            print("\n\033[1;31mArquivo inválido\033[0;0m")
            continue

        AFs.append(af)

        print(f"\n\033[1;32mAutômato {af.name} importado!\033[0;0m")

    elif op == 2:
        print(f"\n------- VISUALIZAÇÃO DE AUTÔMATO -------\n")
        for i, af in enumerate(AFs):
            print(f"{i+1}- {af.name}")
        
        try:
            afId = int(input("\nEscolha o autômato: ")) - 1
            assert(afId in range(0, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
        
        print(f"\nTabela de transição de {AFs[afId].name}:\n")
        AFs[afId].plot()

        input("Pressione enter para continuar...")

    elif op == 3:
        print(f"\n------- EXPORTAR AUTÔMATO -------\n")
        for i, af in enumerate(AFs):
            print(f"{i+1}- {af.name}")
        
        try:
            afId = int(input("\nEscolha o autômato: ")) - 1
            assert(afId in range(0, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
        nameAF = AFs[afId].name
        AFs[afId].exportAF(f"testes/{nameAF}.txt")
        
        print(f"\n\033[1;32mAutômato {nameAF} exportado!\033[0;0m")
        
    elif op == 4:
        print(f"\n--------- REMOÇÃO DE AUTÔMATO ---------\n")
        for i, af in enumerate(AFs):
            print(f"{i+1}- {af.name}")

        try:        
            afId = int(input("\nEscolha o autômato (0 para cancelar): ")) - 1
            assert(afId in range(-1, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
        
        if afId < 0:
            continue

        afName = AFs[afId].name

        del AFs[afId]

        print(f"\n\033[1;32mAutômato {afName} removido!\033[0;0m")

    elif op == 5:
        print(f"\n----- DETERMINIZAÇÃO DE AUTÔMATO -----\n")
        for i, af in enumerate(AFs):
            print(f"{i+1}- {af.name}")
        
        try:
            afId = int(input("\nEscolha o autômato: ")) - 1
            assert(afId in range(0, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
    
        afd = AFs[afId].getAFD()

        print(f"Autômato {AFs[afId].name} determinizado:\n")
        afd.plot()

        save = input("\nSalvar resultado (s/n)? ").strip()

        if save == 's':
            afd.name = input("\nNome do novo autômato: ")
            AFs.append(afd)

            print(f"\n\033[1;32mAutômato {afd.name} inserido!\033[0;0m")
            
    elif op == 6:
        print(f"\n----- RECONHECIMENTO DE SENTENÇA -----\n")
        for i, af in enumerate(AFs):
            print(f"{i+1}- {af.name}")
        
        try:
            afId = int(input("\nEscolha o autômato: ")) - 1
            assert(afId in range(0, len(AFs)))
            af = AFs[afId]
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
    
        sentence = input("\nSentença: ")

        if af.compute(sentence):
            print(f"\n\033[1;32mAutômato {af.name} reconhece {sentence}!\033[0;0m")
        else:
            print(f"\n\033[1;31mAutômato {af.name} não reconhece {sentence}!\033[0;0m")

    elif op == 7:
        print(f"\n------- MINIMIZAÇÃO DE AUTÔMATO ------\n")
        for i, af in enumerate(AFs):
            print(f"{i+1}- {af.name}")
        
        try:
            afId = int(input("\nEscolha o autômato: ")) - 1
            assert(afId in range(0, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
    
        afd = AFs[afId].minimize()

        print(f"Autômato {AFs[afId].name} minimizado:\n")
        afd.plot()

        save = input("\nSalvar resultado (s/n)? ").strip()

        if save == 's':
            afd.name = input("\nNome do novo autômato: ")
            AFs.append(afd)

            print(f"\n\033[1;32mAutômato {afd.name} inserido!\033[0;0m")
    elif op == 8:
        print(f"\n------- UNIÃO DE AUTÔMATOS FINITOS DETERMINÍSTICOS -------\n")
        
        for i, af in enumerate(AFs):
            print(f"{i+1}- {af.name}")
        try:
            afId1 = int(input("\nEscolha primeiro o autômato: ")) - 1
            assert(afId1 in range(0, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
        
        for i, af in enumerate(AFs):
            if i == afId1: continue
            print(f"{i+1}- {af.name}")
        try:
            afId2 = int(input("\nEscolha segundo o autômato: ")) - 1
            assert(afId1 in range(0, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue

        print("\nVocê escolheu os seguintes AFDs:\n")
        print(f"\n{AFs[afId1].name}:\n")
        AFs[afId1].plot()
        print(f"\n{AFs[afId2].name}:\n")
        AFs[afId2].plot()

        print("União:")
        af_union = union(AFs[afId1], AFs[afId2])
        af_union.plot()

        save = input("\nSalvar resultado (s/n)? ").strip()

        if save == 's':
            af_union.name = input("\nNome do novo autômato: ")
            AFs.append(af_union)

            print(f"\n\033[1;32mAutômato {af_union.name} inserido!\033[0;0m")
            
        input("Pressione enter para continuar...")

    elif op == 9:
        
        print(f"\n------- INTERSEÇÃO DE AUTÔMATOS FINITOS DETERMINÍSTICOS -------\n")
        
        for i, af in enumerate(AFs):
            print(f"{i+1}- {af.name}")
        try:
            afId1 = int(input("\nEscolha primeiro o autômato: ")) - 1
            assert(afId1 in range(0, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
        
        for i, af in enumerate(AFs):
            if i == afId1: continue
            print(f"{i+1}- {af.name}")
        try:
            afId2 = int(input("\nEscolha segundo o autômato: ")) - 1
            assert(afId1 in range(0, len(AFs)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue

        print("\nVocê escolheu os seguintes AFDs:\n")
        print(f"\n{AFs[afId1].name}:\n")
        AFs[afId1].plot()
        print(f"\n{AFs[afId2].name}:\n")
        AFs[afId2].plot()

        print("União:")
        af_intersection = intersection(AFs[afId1], AFs[afId2])
        af_intersection.plot()

        save = input("\nSalvar resultado (s/n)? ").strip()

        if save == 's':
            af_intersection.name = input("\nNome do novo autômato: ")
            AFs.append(af_intersection)

            print(f"\n\033[1;32mAutômato {af_intersection.name} inserido!\033[0;0m")
            
        input("Pressione enter para continuar...")

    elif op == 10:
        print(f"\n-------- CONVERSÃO ER -> AFD --------\n")

        regex = input("Digite a expressão regular: ").strip()

        af = AF()
        af.readRegex(regex)

        print("\nConversão para autômato finito: ")
        af.plot()

        save = input("Deseja salvar o autômato (s/n)? ").strip()

        if save == 's':
            af.name = input("Digite o nome do novo autômato: ").strip()
            AFs.append(af)
    elif op == 11:
        print(f"\n----------- IMPORTAR GRAMÁTICA ----------\n")

        name = input("Nome ds nova gramática: ")
        file = input("Nome do arquivo: ")

        glc = GLC(name=name)

        try:
            glc.readData(f"testes/{file}")
        except:
            print("\n\033[1;31mArquivo inválido\033[0;0m")
            continue

        Grammars.append(glc)

        print(f"\n\033[1;Gramática {glc.name} importado!\033[0;0m")

    elif op == 12:
        print(f"\n------- VISUALIZAÇÃO DE GRAMÁTICA -------\n")
        for i, glc in enumerate(Grammars):
            print(f"{i + 1}- {glc.name}")

        try:
            glcId = int(input("\nEscolha a gramática: ")) - 1
            assert (glcId in range(0, len(Grammars)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue

        print(f"\nProduções de {Grammars[glcId].name}:\n")
        print(Grammars[glcId])

        input("Pressione enter para continuar...")
    elif op == 13:
        print(f"\n--------- REMOÇÃO DE AUTÔMATO ---------\n")
        for i, glc in enumerate(Grammars):
            print(f"{i + 1}- {glc.name}")

        try:
            glcId = int(input("\nEscolha o autômato (0 para cancelar): ")) - 1
            assert (glcId in range(-1, len(Grammars)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue

        if glcId < 0:
            continue

        name = Grammars[glcId].name

        del Grammars[glcId]

        print(f"\n\033[1;32mAutômato {name} removido!\033[0;0m")

    elif op == 14:
        print(f"\n------- EXPORTAR GRAMÁTICA -------\n")
        for i, glc in enumerate(Grammars):
            print(f"{i + 1}- {glc.name}")

        try:
            glcId = int(input("\nEscolha a gramática: ")) - 1
            assert (glcId in range(0, len(Grammars)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue
        name = Grammars[glcId].name
        Grammars[glcId].export(f"testes/{name}.txt")

        print(f"\n\033[1;32mAutômato {name} exportado!\033[0;0m")

    elif op == 15:
        ...
    elif op == 16:
        print(f"\n----- FATORAÇÃO -----\n")
        for i, grammar in enumerate(Grammars):
            print(f"{i + 1}- {grammar.name}")

        try:
            grammarId = int(input("\nEscolha a gramática: ")) - 1
            assert (grammarId in range(0, len(Grammars)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue

        grammar = copy.copy(Grammars[grammarId])
        grammar.left_factoring()
        print(grammar)

        save = input("Deseja salvar a gramática (s/n)? ").strip()

        if save == 's':
            grammar.name = input("Digite o nome do novo autômato: ").strip()
            Grammars.append(grammar)
        
    elif op == 17:
        ...
    elif op == 18:
        print(f"\n----- RECONHECIMENTO DE SENTENÇA COM SLR(1) -----\n")
        for i, grammar in enumerate(Grammars):
            print(f"{i+1}- {grammar.name}")
        
        try:
            grammarId = int(input("\nEscolha a gramática: ")) - 1
            assert(grammarId in range(0, len(Grammars)))
        except:
            print("\n\033[1;31mValor inválido\033[0;0m")
            continue

        grammar = Grammars[grammarId]

        sentence = input("Digite a sentença com símbolos separados por espaço: ").strip()

        if grammar.slrRecognizeSentence(sentence):
            print(f"\n\033[1;32mGramática {grammar.name} reconhece {sentence}!\033[0;0m")
        else:
            print(f"\n\033[1;31mGramática {grammar.name} não reconhece {sentence}!\033[0;0m")

    else:
        break
