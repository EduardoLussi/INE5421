from AF import AF

AFs = []    # Lista de autômatos

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
    print("11- Sair")

    op = int(input("\nEscolha uma opção: "))

    if op == 1:
        print(f"\n----------- IMPORTAR AUTÔMATO ----------\n")

        name = input("Nome do novo autômato: ")
        file = input("Nome do arquivo: ")

        af = AF(name=name)

        try:
            af.readData(f"AFs/{file}")
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
        ...

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
        ...
    elif op == 8:
        ...
    elif op == 9:
        ...
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

    else:
        break
