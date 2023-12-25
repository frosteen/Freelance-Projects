
Neutrophil = 0
Lympocyte = 0
Monocyte = 0
Eosinophil = 0
Basophil = 0

import numpy as np
classes = np.array([0,1,3,1,0,0,1,1,1,0,1,1,1,0,0,0,0,1,1,3,0,3,1,0,0,0,3,3,1,1,0,1,0,0,1,0,1,
1,0,0,1,0,1,0,0,3,1,0,0,0,1,0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0,1,1,0,1,3,0,0,
1,1,1,1,0,0,1,0,1,0,0,1,2,0,1,0,3,0,1,0,1,0,0,0,0,0])
print(len(classes))
##classes = np.array([0,1,0,3,3,1,3,3,0,1,1,2,3,2,4])
classesOrig = classes.tolist().copy()
classes = list(dict.fromkeys(classes))
classes.sort(reverse=True)
print(classes)
totalCells = len(classesOrig)
ordered = []
for x in classes:
    ordered.append(classesOrig.count(x))
ordered.sort(reverse=True)
if len(ordered) > 0:
    Neutrophil = (ordered[0]/totalCells)*100
if len(ordered) > 1:
    Lympocyte = (ordered[1]/totalCells)*100
if len(ordered) > 2:
    Monocyte = (ordered[2]/totalCells)*100
if len(ordered) > 3:
    Eosinophil = (ordered[3]/totalCells)*100
if len(ordered) > 4:
    Basophil = (ordered[4]/totalCells)*100
print(Neutrophil, Lympocyte, Monocyte, Eosinophil, Basophil)
