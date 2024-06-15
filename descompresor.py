import sys
import bitarray as bit

def cargarDiccionario(archTabla):
    diccionario = {}
    caminoAux = ""
    with open(archTabla,"r",encoding="utf-8") as arch:

        for linea in arch:

            if linea == "\n":
                break

            simbolo,camino = linea.split(": ")

            for i in range(len(camino)-1):
                caminoAux += camino[i]

            if simbolo == "φ":
                diccionario[caminoAux] = "\n"
                caminoAux = ""
            else:
                diccionario[caminoAux] = simbolo
                caminoAux = ""

    return diccionario


def descompresor(input,archTabla,output):
    diccionario = cargarDiccionario(archTabla)
    bitStr = bit.bitarray()

    with open(input,"rb") as arch:
        bitStr.fromfile(arch)
    
    textoDecod = ""
    bitsActuales = ""

    for bits in bitStr:

        if bits:
            bitsActuales += "1"
        else:
            bitsActuales += "0"
        
        if bitsActuales in diccionario:
            textoDecod += diccionario[bitsActuales]
            bitsActuales = ""
    
    with open(output,"w",encoding="utf-8") as arch:
        arch.write(textoDecod)


descompresor("himnoUSA.txt.huff","himnoUSA.txt.table","outputDesc.txt")