import sys
import bitarray as bit


def sacarFrecuencias(input):

    frecuencias = {}

    with open(input,"r",encoding="utf-8") as arch:
        while True:
            char = arch.read(1)

            if char == "":
                break

            if char == "\n":
                if char in frecuencias:
                    frecuencias["φ"] += 1
                else:
                    frecuencias["φ"] = 1

            else:
                if char in frecuencias:
                    frecuencias[char] += 1
                else:
                    frecuencias[char] = 1
            
    return frecuencias



def trie(frecuencias):
    
    arbol = [[frecuencias[i], i] for i in frecuencias]
    
    while len(arbol) > 1:

        arbol.sort(key=lambda nods: nods[0])
        izq = arbol.pop(0)
        der = arbol.pop(0)

        nodos = [izq[0]+der[0],izq,der]
        arbol.append(nodos)

    return arbol[0]



def diccionarioHuff(arbolHuff):
    diccionario = {}
    pila = [(arbolHuff,"")]

    while pila:
        
        arbol,camino = pila.pop()

        if type(arbol[1]) == str:
            diccionario[arbol[1]] = camino
        
        else:
            _,izq,der = arbol

            if izq:
                pila.append((izq, camino + "0"))

            if der:
                pila.append((der, camino + "1"))
        
    return diccionario


def altura(arbolHuff):

    if type(arbolHuff[1]) == str:
        return 0
    
    T,izq,der = arbolHuff

    ladoI = altura(izq)+1
    ladoD = altura(der)+1

    return max(ladoI,ladoD)


def anchura(arbolHuff):
    
    tamNiv = 0
    maxAncho = 0
    cola = [arbolHuff]

    while cola:

        for i in range(len(cola)):
            T,izq,der = cola.pop(0)

            if type(izq[1]) != str:
                cola.append(izq)
            if type(der[1]) != str:
                cola.append(der)

            tamNiv += 2

        maxAncho = max(maxAncho,tamNiv)
        tamNiv = 0

    return maxAncho



def nodos_por_nivel(arbolHuff):
    
    niv = 0
    niveles = [0]*(altura(arbolHuff)+1)
    niveles[niv] = 1
    cola = [(arbolHuff,niv+1)]

    while cola:

        for i in range(len(cola)):
            arbol,niv = cola.pop(0)

            if type(arbol[1][1]) != str:
                cola.append((arbol[1],niv+1))
            if type(arbol[2][1]) != str:
                cola.append((arbol[2],niv+1))
            niveles[niv] += 2

    return niveles



def archivoTabla(diccionario,archTabla):

    with open(archTabla,"w",encoding="utf-8") as arch:
        
        for simbolo,camino in diccionario.items():
            arch.write(f"{simbolo}: {camino}\n")


def archivoStats(stats,archStats):

    with open(archStats,"w",encoding="utf-8") as arch:

        for nombre,valor in stats.items():
            arch.write(f"{nombre}: {valor}\n")


def comprimirArchivo(input,output,diccionario):
    bitStr = bit.bitarray()

    with open(input,"r",encoding='utf-8') as arch:
        while True:
            char = arch.read(1)

            if char == "":
                break

            if char == "\n":
                bitStr.extend(diccionario["φ"])
            else:
                bitStr.extend(diccionario[char]) # Podria ser .extend si no sirve

    with open(output,"wb") as arch:
        bitStr.tofile(arch)



def tablaFrecuencia(frecuencias):
    tabla = ""

    for simbolo,valor in frecuencias.items():
        tabla += f"\n{simbolo}: {valor}"
    
    return tabla



def compresor_principal(input):
    frecuencia = sacarFrecuencias(input)
    arbolHuff = trie(frecuencia)
    diccionario = diccionarioHuff(arbolHuff)

    arch_output = input + ".huff"
    arch_tabla = input + ".table"
    arch_stats = input + ".stats"

    comprimirArchivo(input,arch_output,diccionario)
    archivoTabla(diccionario,arch_tabla)

    stats = {
        "Altura del árbol": altura(arbolHuff),
        "Anchura del árbol": anchura(arbolHuff),
        "Cantidad de nodos por nivel": nodos_por_nivel(arbolHuff),
        "Tabla de frecuencias original": tablaFrecuencia(frecuencia)
    }

    archivoStats(stats,arch_stats)



compresor_principal(sys.argv[1])

