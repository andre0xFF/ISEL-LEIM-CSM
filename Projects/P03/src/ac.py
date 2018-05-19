import pprint
pp = pprint.PrettyPrinter(indent=4)

def getSize(amplitude: int, positive: bool) -> (int, int):
    return amplitude, len("{0:b}".format(np.abs(amplitude)))  
    
    
print("Imagem ANTES de ser aplicada a DCT bidimensional:")
input_file = "../data/raw/Lena.tif"
plt.figure(figsize=(5,5))
image = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE)*1.0
plt.imshow(image, cmap='gray')
plt.show()

#Aplicar Bloco final a imagem construindo a imagem comprimida
submatriz = codificacaoJPEG(image).astype("int")

submatriz = np.array([
                        [ 84,  5, -3,  1,  3, -1,  1,  0],
                        [ -3, -2,  1,  2,  1,  0,  0,  0],
                        [ -1, -1,  1,  1,  1,  0,  0,  0],
                        [ -1,  0,  0,  1,  0,  0,  0,  0],
                        [  0,  0,  0,  0,  0,  0,  0,  0],
                        [  0,  0,  0,  0,  0,  0,  0,  0],
                        [  0,  0,  0,  0,  0,  0,  0,  0],
                        [  0,  0,  0,  0,  0,  0,  0,  0]
                                                                    ])
print("ORIGINAL SUBMATRIZ")
print(submatriz)
print("\n")
submatriz = submatriz.flatten(order='F')
submatriz = submatriz[ind_Z]
print("ZIGZAG SUBMATRIZ FLATTEN")
print(submatriz)
print("\n")

e = dict()
f = []

countzeros = 0
for i in range(1, len(submatriz) - 1):
    if submatriz[i] == 0:
        countzeros += 1
    elif submatriz[i] > 0:
        size, amplitude = getSize(submatriz[i], True)
        e[i] = [(countzeros, amplitude), size]
        countzeros = 0
    elif submatriz[i] < 0:
        size, amplitude = getSize(submatriz[i], False)
        e[i] = [(countzeros, amplitude), size]
        countzeros = 0
    e[len(submatriz) - 1] = [(0, 0), 0]

print("______________________________________________________")

print("AC IN INTEGER")
pp.pprint(e)
print("\n")

countzeros = 0
for i in range(1, len(submatriz) - 1):
    if submatriz[i] == 0:
        countzeros += 1
    elif submatriz[i] > 0:
        size, amplitude = getSize(submatriz[i], True)
        valueK5 = K5[(countzeros, amplitude)]
        binaryAmplitude = "0" + "{0:b}".format(np.abs(size))
        f += valueK5 + binaryAmplitude
        print("valueK5")
        print(valueK5)
        print("binaryAmplitude")
        print(binaryAmplitude)
        countzeros = 0
    elif submatriz[i] < 0:
        size, amplitude = getSize(submatriz[i], True)
        valueK5 = K5[(countzeros, amplitude)]
        binaryAmplitude = "1" + "{0:b}".format(np.abs(size))
        print("valueK5")
        print(valueK5)
        print("binaryAmplitude")
        print(binaryAmplitude)
        f += valueK5 + binaryAmplitude
        countzeros = 0
f += "000"   


print("______________________________________________________")

g = ""
for c in f:
    g += c
print("AC FROM BITSTREAM")
print(g)
print("\n")

dimensions = [len(v) for v in K5.values()] 
print("DIMENSIONS")
print(dimensions)
print("\n")

dict_values = list(K5.values())
print("DICT VALUES")
print(dict_values)
print("\n")

dict_keys = list(K5.keys())
print("DICT KEYS")
print(dict_keys)
print("\n")

min_size = min(map(len, dict_values))
decoded = []
print("\n")
print("dict_keys[0]")
print(dict_keys[0])
print(len(dict_keys))
print("\n")

print("AC BINARY FORMAT")
print(g)
print("\n")

def convertBackToInt(binary: str, positive: bool = True):
    if binary != "0":
        binary = binary[1:]
        backToInt = int(binary, 2)
        if not positive:
            backToInt *= -1
        return backToInt
    else:
        return 0
    
    
i = 0
j = 1
while((len(g) > 0) and i < 80):
    i +=1
    if(i in dimensions):
        for v in range(len_dict_values):
            if(len(g[:i]) == len(dict_values[v])):
                print("Comparing...")
                print(g[:i])
                print("... to...")
                print(dict_values[v])
                
                if(g[:i] == dict_values[v]):
                    zero_run_length = dict_keys[v][0]
                    if(zero_run_length != 0):
                        for h in range(zero_run_length):
                            decoded.append(0)
                        print("ADDED " + str(zero_run_length) + " ZEROS")
                        print(decoded)
                        
                    nrbits = dict_keys[v][1] + 1 #mais bit de sinal
                    print("index position")
                    print(i)
                    print("nrbits to read next...")
                    print(nrbits)
                    binaryString = g[i : i + nrbits]
                    print("value being analysed...")
                    print(binaryString)
                    if binaryString[0] != "0":
                        backToInt = convertBackToInt(binaryString, False)
                    else:
                        backToInt = convertBackToInt(binaryString, True)
                    print("resulting integer...")
                    print(backToInt)
                    decoded.append(backToInt)
                    print(decoded)
                    print("::::")
                    print(g)
                    g = g[i + nrbits:]
                    print("::::")
                    print(g)
                    j += 1
                    i = min_size-1
                    break
while(len(decoded) < 64):
    decoded.append(0)
    
    
print("AC TUPLE FORMAT")
pp.pprint(e)
print("\n")

print("DECODED BLOCK")
print(decoded)
print("\n")

print("ORIGINAL SUBMATRIZ")
submatriz = submatriz[ind_O].reshape((8,8),order='F')
print(submatriz)
print("\n")
