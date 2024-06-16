import sys
import bitarray as bit

#Dominio: El archivo con la tabla de frecuencias de cada carácter del archivo original .table
#Codominio: Un diccionario 
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

#Dominio: El archivo comprimido .huff, el archivo con la tabla de frecuencias .table, y un archivo donde se va a escribir el contenido del archivo original del .huff
#Codominio: El archivo output con el contenido del archivo original
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


descompresor(sys.argv[1],sys.argv[2],"outputDesc.txt")