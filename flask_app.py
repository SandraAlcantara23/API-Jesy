from flask import Flask, jsonify, render_template
import math
import random

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

# Función para calcular la distancia entre dos coordenadas (usando la fórmula de distancia Euclidiana)
def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# Función para evaluar una ruta y obtener su distancia total
def evalua_ruta(ruta, coord):
    total = 0
    for i in range(0, len(ruta)-1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[-1]
    ciudad2 = ruta[0]
    total += distancia(coord[ciudad1], coord[ciudad2])
    return total

# Algoritmo Hill Climbing para encontrar la mejor ruta
def i_hill_climbing(coord):
    ruta = list(coord.keys())
    random.shuffle(ruta)
    
    mejor_ruta = ruta[:]
    dist_mejor_ruta = evalua_ruta(mejor_ruta, coord)
    
    max_iteraciones = 10
    
    while max_iteraciones > 0:
        mejora = True
        
        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta, coord)
            
            for i in range(len(ruta)):
                if mejora:
                    break
                for j in range(len(ruta)):
                    if i != j:
                        ruta_tmp = ruta[:]
                        # Intercambiar las posiciones i y j
                        ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                        
                        dist_tmp = evalua_ruta(ruta_tmp, coord)
                        if dist_tmp < dist_actual:
                            mejora = True
                            ruta = ruta_tmp[:]
                            break
        
        if evalua_ruta(ruta, coord) < dist_mejor_ruta:
            mejor_ruta = ruta[:]
            dist_mejor_ruta = evalua_ruta(mejor_ruta, coord)
        
        max_iteraciones -= 1
        
    return mejor_ruta

# Ruta principal (Home) - Mostramos la página HTML
@app.route('/')
def home():
    return render_template("index.html")

# Ruta para obtener la mejor ruta (en formato JSON)
@app.route('/mejor_ruta', methods=['GET'])
def obtener_mejor_ruta():
    coord = {
        'Jiloyork': (19.916012, -99.580580),
        'Toluca': (19.289165, -99.655697),
        'Atlacomulco': (19.799520, -99.873844),
        'Guadalajara': (20.677754472859146, -103.34625354877137),
        'Monterrey': (25.69161110159454, -100.321838480256),
        'QuintanaRoo': (21.163111924844458, -86.80231502121464),
        'Michoacan': (19.701400113725654, -101.20829680213464),
        'Aguascalientes': (21.87641043660486, -102.26438663286967),
        'CDMX': (19.432713075976878, -99.13318344772986),
        'QRO': (20.59719437542255, -100.38667040246602)
    }
    
    mejor_ruta_final = i_hill_climbing(coord)
    distancia_total = evalua_ruta(mejor_ruta_final, coord)
    
    return jsonify({
        "mejor_ruta": mejor_ruta_final,
        "distancia_total": round(distancia_total, 6)
    })

if __name__ == "__main__":
    app.run(debug=True)



