from AF import AF

# Miniteste 3 sem epsilon
K = ['p', 'q', 'r', 's']
sigma = ['0', '1']
delta = [('p', '0', 'p'), ('p', '0', 'q'), ('p', '1', 'p'),
         ('q', '0', 'r'), ('q', '1', 'r'),
         ('r', '0', 's'),
         ('s', '0', 's'), ('s', '1', 's')]
s = 'p'
F = ['s']

automata = AF(K, sigma, delta, s, F)
automata.plot()
automata = automata.getAFD()
automata.plot()

# Miniteste 3 com epsilon
K = ['p', 'q', 'r']
sigma = ['&', 'a', 'b', 'c']
delta = [('p', 'a', 'p'), ('p', 'b', 'q'), ('p', 'c', 'r'),
         ('q', '&', 'p'), ('q', 'a', 'q'), ('q', 'b', 'r'),
         ('r', '&', 'q'), ('r', 'a', 'r'), ('r', 'c', 'p')]
s = 'p'
F = ['r']

automata = AF(K, sigma, delta, s, F)
automata.plot()
automata = automata.getAFD()
automata.plot()