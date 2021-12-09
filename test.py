from AF import AF

automata = AF()
automata.readData("test.txt")
#automata.plot()
print(automata.compute("0001101"))
