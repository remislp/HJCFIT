""" Holds some general setup for behave. """

def Matrix(string): 
  """ Creates matrices from specific strings """
  from numpy import array, identity
  from dcprogs.random import qmatrix as random_qmatrix
  if string == "classic":
    return array([[ -3050,        50,  3000,      0,    0 ], 
                  [ 2./3., -1502./3.,     0,    500,    0 ],  
                  [    15,         0, -2065,     50, 2000 ],  
                  [     0,     15000,  4000, -19000,    0 ],  
                  [     0,         0,    10,      0,  -10 ] ])
  if string == "empty": return array([])
  if string == "spam": return identity(5).tolist()
  if string == "numpy_spam": return array([['a', 'b', 'c']*3])
  if string == "rectangle": return identity(6).reshape(3, 12)
  if string == "complex eigenvalues": 
    return array([ [-3466.42238140472, 0, 1469.750247214199, 0, 0, 0, 0, 1996.248289012859,
                     0, 0.4238451776618666, 0, 0, 0, 0, 0, 0, 0],
                   [ 0, -1.194504097606079, 0, 0, 0.460207514804313, 0, 0.2214267875326077,
                     0, 0, 0, 0, 0, 0, 0.5128697952691581, 0, 0, 0],
                   [ 0.3310137074523044, 0, -3820.99564314745, 0, 0, 0, 1429.255679060063,
                     0, 0, 0, 0, 0, 0, 0, 0, 2390.617610721906,  0.7913396580283524],
                   [ 0, 0, 0, -1147.335097261639, 0.4181705791411652, 0.3689750475587887,
                     0, 0, 0.8450135899657636, 0, 0, 1144.487515010296, 0, 0, 0, 0.8480896174403655,
                     0.367333417236442],
                   [ 0, 0.7563419288555676, 0, 0.9407263983990233, -2268.341855964324, 0, 0, 0,
                     0, 0.536509226640146, 0, 0, 2265.341787266065, 0, 0, 0,  0.7664911443640284],
                   [ 0, 0, 0,  0.9716559216308585, 0, -2.939644707388761, 0.7758977585984975,
                     0, 0.04878840707929973, 0.9274838037659627, 0, 0, 0.2158188163141428,
                     0, 0, 0, 0],
                   [ 0, 0.2426842584232713, 0.5709976405655057, 0, 0, 1501.393808251859,
                     -4947.866138869221, 0, 0, 2967.530324405681,   477.8671954868795,
                     0, 0,   0.152582620081897, 0,  0.1085462057298684, 0],
                   [ 0.1116651856585598, 0, 0, 0, 0, 0, 0, -0.6172465503726881, 0, 0, 0,
                     0.5055813647141282, 0, 0, 0, 0, 0],
                   [ 0, 0, 0, 10.70846772714012, 0, 0.8755908206602385, 0, 0, -13.39834640597427, 0,
                     0, 0.4956333464228559,  0.8843507172966485, 0, 0.4343037944544128,
                     0, 0],
                   [ 0.7031054301958579, 0, 0, 0, 0.8767229348612872,  0.1010550024986546,
                     0.7039982751675876, 0, 0, -1390.92968416444, 0.5872281168852814, 0, 0,
                     1387.957574404831, 0, 0, 0],
                   [ 0, 0, 0, 0, 0, 0, 0.2616980112563155, 0, 0, 0.5974848073393281,
                     -1423.484834980496, 0, 0, 0, 1421.917836692536, 0, 0.7078154693645349],
                   [ 0, 0, 0, 0.07315515350855138, 0, 0, 0,  0.3548322889802194,
                     0.1600589507619137, 0, 0, -1.547721538787326,  0.8963384481862553,
                     0, 0.06333669735038627, 0, 0],
                   [ 0, 0, 0, 0, 0.3347280997700345, 0.09007341889982411, 0, 0,  0.4719510050316036,
                     0, 0, 0.6375616697058537,  -1.534314193407316, 0, 0, 0, 0],
                   [ 0, 0.5131288725680503, 0, 0, 0, 0, 0.8191330026813676, 0, 0,
                     0.7856276269785871, 0, 0, 0, -2.117889502228005, 0, 0, 0],
                   [ 0, 0, 0, 0, 0, 0, 0, 0,  0.3480547057289432, 0, 0.5960842400582568,
                     0.2000879995337751, 0, 0, -1.350938009623582,  0.2067110643026069, 0],
                   [ 0, 0, 0.2340883417220923, 0.9660592873591691, 0, 0, 0.9358095813718609,
                     0, 0, 0, 0, 0, 0, 0,  0.7293365597204913, -3.279096956555216,
                     0.4138031863816024],
                   [ 0, 0, 0.5958562312957759, 0.8349824944924248, 21.78352763660896,
                     0, 0, 0, 0, 0, 0.8079999622957483, 0, 0, 0, 0, 0.2303859780888245,
                     -24.25275230278173]])
  if string == "singular matrix":
    return array([[ -8.60862871e+03,   0.00000000e+00,   0.00000000e+00, 8.60862871e+03,
                     0.00000000e+00,   0.00000000e+00, 0.00000000e+00],
                  [  0.00000000e+00,  -5.63832745e+03,   0.00000000e+00, 0.00000000e+00,
                     5.63832745e+03,   0.00000000e+00, 0.00000000e+00],
                  [  0.00000000e+00,   0.00000000e+00,  -5.43772860e+04, 0.00000000e+00,
                     0.00000000e+00,   5.43772860e+04, 0.00000000e+00],
                  [  1.18958719e+05,   0.00000000e+00,   0.00000000e+00, -1.24208820e+05,
                     3.39628323e+03,   1.85381780e+03, 0.00000000e+00],
                  [  0.00000000e+00,   6.77847125e+01,   0.00000000e+00, 1.01956162e+01,
                     -1.93179812e+03,   0.00000000e+00, 1.85381780e+03],
                  [  0.00000000e+00,   0.00000000e+00,   8.14133272e+01, 6.00000000e+00,
                     0.00000000e+00,  -3.48369656e+03, 3.39628323e+03],
                  [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, 0.00000000e+00,
                     6.00000000e+00,   1.01956162e+01, -1.61956162e+01]])
  if string == "random": return random_qmatrix()

def StatMat(string):
  """ Creates matrices from specific strings """
  from dcprogs.random import state_matrix as random_state_matrix
  from dcprogs.likelihood import StateMatrix
  if string == "classic": return StateMatrix(Matrix(string), 2)
  if string == "complex eigenvalues": return StateMatrix(Matrix(string), 4)
  if string == "singular matrix": return StateMatrix(Matrix(string), 3)
  if string == "random": return random_state_matrix()
  else: raise Exception("Unknown State Matrix {0}".format(string))

def register_type(): 
  from behave import matchers
  matchers.register_type(Integer=lambda x: int(x))
  matchers.register_type(Float=lambda x: float(x))
  matchers.register_type(Eval=lambda x: eval(x))
  matchers.register_type(Bool=lambda x: bool(x))
  matchers.register_type(Matrix=Matrix)
  matchers.register_type(StatMat=StatMat)
