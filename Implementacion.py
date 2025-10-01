def leer_gramatica(ruta_archivo):
    gramatica = {}
    
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if '->' in linea:
                cabeza, producciones = linea.split('->')
                cabeza = cabeza.strip()
                producciones = [prod.strip().replace('lambda', 'ε').split() for prod in producciones.split('|')]
                if cabeza not in gramatica:
                    gramatica[cabeza] = []
                gramatica[cabeza].extend(producciones)
    return gramatica

def calcular_primeros(gramatica):
    primeros = {nt: set() for nt in gramatica}

    def obtener_primeros(simbolo):
        if simbolo not in gramatica:
            return {simbolo}
        if primeros[simbolo]:
            return primeros[simbolo]
        for produccion in gramatica[simbolo]:
            for prod_simbolo in produccion:
                prod_primeros = obtener_primeros(prod_simbolo)
                primeros[simbolo].update(prod_primeros - {'ε'})
                if 'ε' not in prod_primeros:
                    break
            else:
                primeros[simbolo].add('ε')
        return primeros[simbolo]

    for nt in gramatica:
        obtener_primeros(nt)
    return primeros

def calcular_primeros_cadena(cadena, primeros_dict):
    if not cadena:
        return {'ε'}
    
    resultado = set()
    todos_epsilon = True
    
    for simbolo in cadena:
        if simbolo in primeros_dict:
            resultado.update(primeros_dict[simbolo] - {'ε'})
            if 'ε' not in primeros_dict[simbolo]:
                todos_epsilon = False
                break
        else:
            resultado.add(simbolo)
            todos_epsilon = False
            break
    
    if todos_epsilon:
        resultado.add('ε')
    
    return resultado

def calcular_siguientes(gramatica, primeros_dict):
    siguientes = {nt: set() for nt in gramatica}
    simbolo_inicial = list(gramatica.keys())[0]
    siguientes[simbolo_inicial].add('$')
    cambiado = True
    
    while cambiado:
        cambiado = False
        for cabeza, producciones in gramatica.items():
            for produccion in producciones:
                for i, simbolo in enumerate(produccion):
                    if simbolo in gramatica:
                        tamaño_anterior = len(siguientes[simbolo])
                        resto = produccion[i+1:]
                        primeros_resto = calcular_primeros_cadena(resto, primeros_dict)
                        siguientes[simbolo].update(primeros_resto - {'ε'})
                        if 'ε' in primeros_resto:
                            siguientes[simbolo].update(siguientes[cabeza])
                        if len(siguientes[simbolo]) > tamaño_anterior:
                            cambiado = True
    return siguientes

def calcular_predicciones(gramatica):
    primeros_dict = calcular_primeros(gramatica)
    siguientes_dict = calcular_siguientes(gramatica, primeros_dict)
    predicciones = {cabeza: {} for cabeza in gramatica}

    for cabeza, producciones in gramatica.items():
        for produccion in producciones:
            prediccion = set()
            primeros_produccion = calcular_primeros_cadena(produccion, primeros_dict)
            prediccion.update(primeros_produccion - {'ε'})
            if 'ε' in primeros_produccion:
                prediccion.update(siguientes_dict[cabeza])
            predicciones[cabeza][tuple(produccion)] = prediccion

    return predicciones

# FUNCIONES PRINCIPALES

def mostrar_primeros(ruta_archivo):
    gramatica = leer_gramatica(ruta_archivo)
    primeros_resultado = calcular_primeros(gramatica)
    
    print("Conjuntos de Primeros:")
    for nt, primeros in primeros_resultado.items():
        print(f"Primeros({nt}): {primeros}")
    
    return primeros_resultado

def mostrar_siguientes(ruta_archivo):
    gramatica = leer_gramatica(ruta_archivo)
    primeros_dict = calcular_primeros(gramatica)
    siguientes_dict = calcular_siguientes(gramatica, primeros_dict)
    
    print("Conjuntos de Siguientes:")
    for nt, conj in siguientes_dict.items():
        print(f"Siguientes({nt}): {conj}")
    
    return siguientes_dict

def mostrar_predicciones(ruta_archivo):
    gramatica = leer_gramatica(ruta_archivo)
    predicciones_resultado = calcular_predicciones(gramatica)
    
    print("Conjuntos de Predicción:")
    for nt, reglas in predicciones_resultado.items():
        for produccion, predicciones_set in reglas.items():
            print(f"Predicción({nt} -> {' '.join(produccion)}): {predicciones_set}")
    
    return predicciones_resultado

def mostrar_todo(ruta_archivo):
    gramatica = leer_gramatica(ruta_archivo)
    
    print("=== GRAMÁTICA ===")
    for nt, prods in gramatica.items():
        print(f"{nt} -> {' | '.join(' '.join(p) for p in prods)}")
    
    print("\nCONJUNTOS DE PRIMEROS ")
    primeros = calcular_primeros(gramatica)
    for nt, conj in primeros.items():
        print(f"Primeros({nt}): {conj}")
    
    print("\n CONJUNTOS DE SIGUIENTES ")
    siguientes = calcular_siguientes(gramatica, primeros)
    for nt, conj in siguientes.items():
        print(f"Siguientes({nt}): {conj}")
    
    print("\n CONJUNTOS DE PREDICCIÓN ")
    predicciones = calcular_predicciones(gramatica)
    for nt, reglas in predicciones.items():
        for produccion, prediccion_set in reglas.items():
            print(f"Predicción({nt} -> {' '.join(produccion)}): {prediccion_set}")


if __name__ == "__main__":
    ruta_archivo = 'Gramatica.txt'
    
    print("ANALIZADOR DE GRAMÁTICA COMPLETO")
    
    mostrar_todo(ruta_archivo)


