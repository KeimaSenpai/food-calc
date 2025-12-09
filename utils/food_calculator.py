"""
Módulo de cálculo de cantidades de comida según normas de consumo.
Uso: from food_calculator import calcular_cantidades_comida, formatear_resultados
"""

def calcular_cantidades_comida(personas):
    """
    Calcula las cantidades necesarias de todos los productos para N personas.
    
    Args:
        personas (int): Número de personas
        
    Returns:
        dict: Diccionario con dos claves:
            - 'productos_kg': dict con productos y cantidades en kg
            - 'productos_unidades': dict con productos y cantidades en unidades
            - 'total_personas': número de personas calculado
    
    Ejemplo:
        >>> resultado = calcular_cantidades_comida(50)
        >>> print(resultado['productos_kg']['Arroz blanco'])
        5.0
    """
    
    # Productos con cantidades en gramos por persona (CRUDO)
    productos_gramos = {
        "Arroz blanco": 100,
        "Arroz moro": 52,
        "Arroz con leche": 10,
        "Frijoles": 45,
        "Carne de cerdo/Fricasé sin hueso": 160,
        "Carne de cerdo/Fricasé con hueso": 250,
        "Pollo/Menudo para sopa": 40,
        "Pollo": 250,
        "Picadillo": 100,
        "Picadillo para albóndiga": 100,
        "Albóndiga": 86,
        "Jamón meriendas": 45,
        "Jamón desayuno": 15,
        "Pescado frito": 140,
        "Pescado aporreado": 100,
        "Carne de res en salsa": 140,
        "Carne de res en ropa vieja": 140,
        "Hígado": 140,
        "Espaguetis Napolitanos": 75,
        "Espaguetis para ensalada": 17,
        "Croquetas (3u)": 120,
        "Croquetas (4u)": 100,
        "Hamburguesa de pollo c/queso": 130,
        "Plátano": 150,
        "Papa": 150,
        "Boniato": 150,
        "Calabaza": 150,
        "Yuca": 150,
        "Tomate": 150,
        "Col": 150,
        "Natilla": 19.2,
        "Gelatina": 19.2,
        "Dulces de latas": 55,
        "Queso para meriendas": 45,
        "Queso para desayuno (Gouda)": 15,
        "Queso para espaguetis": 58,
        "Mantequilla": 8,
        "Mayonesa": 8,
    }
    
    # Productos que se cuentan por unidades
    productos_unidades_base = {
        "Huevo": 2,
        "Huevo revuelto": 1.5,
        "Huevo tortilla": 2,
        "Rodajas de piña": 1,
    }
    
    # Calcular cantidades en kilogramos
    productos_kg = {}
    for producto, gramos_por_persona in productos_gramos.items():
        gramos_totales = gramos_por_persona * personas
        productos_kg[producto] = round(gramos_totales / 1000, 3)
    
    # Calcular cantidades de productos por unidades
    productos_unidades = {}
    for producto, unidades_por_persona in productos_unidades_base.items():
        productos_unidades[producto] = round(unidades_por_persona * personas, 1)
    
    return {
        'productos_kg': productos_kg,
        'productos_unidades': productos_unidades,
        'total_personas': personas
    }


def formatear_resultados(resultado, formato='texto'):
    """
    Formatea los resultados para mostrarlos.
    
    Args:
        resultado (dict): Resultado de calcular_cantidades_comida()
        formato (str): 'texto', 'markdown', 'html' o 'lista'
        
    Returns:
        str o list: Resultados formateados según el formato especificado
    """
    personas = resultado['total_personas']
    productos_kg = resultado['productos_kg']
    productos_unidades = resultado['productos_unidades']
    
    # Categorías para organizar
    categorias = {
        "🍚 ARROCES": ["Arroz blanco", "Arroz moro", "Arroz con leche"],
        "🫘 GRANOS": ["Frijoles"],
        "🍖 CARNES Y AVES": [
            "Carne de cerdo/Fricasé sin hueso",
            "Carne de cerdo/Fricasé con hueso",
            "Pollo/Menudo para sopa",
            "Pollo",
            "Carne de res en salsa",
            "Carne de res en ropa vieja",
            "Hígado"
        ],
        "🍔 PICADILLOS Y ELABORADOS": [
            "Picadillo",
            "Picadillo para albóndiga",
            "Albóndiga",
            "Croquetas (3u)",
            "Croquetas (4u)",
            "Hamburguesa de pollo c/queso"
        ],
        "🐟 PESCADO": ["Pescado frito", "Pescado aporreado"],
        "🥓 EMBUTIDOS": ["Jamón meriendas", "Jamón desayuno"],
        "🍝 PASTAS": ["Espaguetis Napolitanos", "Espaguetis para ensalada"],
        "🥔 VIANDAS": ["Plátano", "Papa", "Boniato", "Calabaza", "Yuca"],
        "🥗 VEGETALES": ["Tomate", "Col"],
        "🍮 POSTRES": ["Natilla", "Gelatina", "Dulces de latas"],
        "🧀 LÁCTEOS": [
            "Queso para meriendas",
            "Queso para desayuno (Gouda)",
            "Queso para espaguetis",
            "Mantequilla"
        ],
        "🥫 CONDIMENTOS": ["Mayonesa"]
    }
    
    if formato == 'lista':
        # Devuelve una lista de diccionarios (útil para APIs/JSON)
        lista = []
        for categoria, productos in categorias.items():
            for producto in productos:
                if producto in productos_kg:
                    lista.append({
                        'categoria': categoria,
                        'producto': producto,
                        'cantidad': productos_kg[producto],
                        'unidad': 'kg'
                    })
        
        for producto, cantidad in productos_unidades.items():
            lista.append({
                'categoria': '🥚 PRODUCTOS POR UNIDADES',
                'producto': producto,
                'cantidad': cantidad,
                'unidad': 'unidades'
            })
        
        return lista
    
    # Formato texto común
    lineas = []
    
    if formato == 'markdown':
        lineas.append(f"**📊 CANTIDADES PARA {personas} PERSONAS**")
        lineas.append(f"*(Producto crudo)*\n")
    elif formato == 'html':
        lineas.append(f"<b>📊 CANTIDADES PARA {personas} PERSONAS</b>")
        lineas.append(f"<i>(Producto crudo)</i>\n")
    else:
        lineas.append(f"📊 CANTIDADES PARA {personas} PERSONAS")
        lineas.append(f"(Producto crudo)\n")
    
    for categoria, productos in categorias.items():
        tiene_productos = False
        items = []
        
        for producto in productos:
            if producto in productos_kg:
                tiene_productos = True
                kg = productos_kg[producto]
                items.append(f"  • {producto}: {kg} kg")
        
        if tiene_productos:
            if formato == 'markdown':
                lineas.append(f"\n**{categoria}**")
            elif formato == 'html':
                lineas.append(f"\n<b>{categoria}</b>")
            else:
                lineas.append(f"\n{categoria}")
            lineas.extend(items)
    
    # Productos por unidades
    if productos_unidades:
        if formato == 'markdown':
            lineas.append(f"\n**🥚 PRODUCTOS POR UNIDADES**")
        elif formato == 'html':
            lineas.append(f"\n<b>🥚 PRODUCTOS POR UNIDADES</b>")
        else:
            lineas.append(f"\n🥚 PRODUCTOS POR UNIDADES")
        
        for producto, unidades in sorted(productos_unidades.items()):
            lineas.append(f"  • {producto}: {unidades} unidades")
    
    return '\n'.join(lineas)


def obtener_producto_especifico(personas, nombre_producto):
    """
    Obtiene la cantidad de un producto específico.
    
    Args:
        personas (int): Número de personas
        nombre_producto (str): Nombre exacto del producto
        
    Returns:
        dict: {'producto': str, 'cantidad': float, 'unidad': str} o None si no existe
    """
    resultado = calcular_cantidades_comida(personas)
    
    if nombre_producto in resultado['productos_kg']:
        return {
            'producto': nombre_producto,
            'cantidad': resultado['productos_kg'][nombre_producto],
            'unidad': 'kg'
        }
    elif nombre_producto in resultado['productos_unidades']:
        return {
            'producto': nombre_producto,
            'cantidad': resultado['productos_unidades'][nombre_producto],
            'unidad': 'unidades'
        }
    
    return None


def listar_productos_disponibles():
    """
    Devuelve una lista de todos los productos disponibles.
    
    Returns:
        list: Lista de nombres de productos
    """
    resultado = calcular_cantidades_comida(1)
    productos = list(resultado['productos_kg'].keys()) + list(resultado['productos_unidades'].keys())
    return sorted(productos)


def obtener_preparaciones_disponibles():
    """
    Devuelve una lista de preparaciones disponibles.
    
    Returns:
        list: Lista de nombres de preparaciones
    """
    preparaciones = {
        "Arroz blanco": {},
        "Arroz moro": {},
        "Frijoles negros": {},
        "Pollo frito": {},
        "Picadillo": {},
        "Espaguetis Napolitanos": {},
        "Plátanos maduros fritos": {},
        "Viandas hervidas (Papa/Yuca/Boniato)": {},
        "Ensalada de col": {},
        "Huevos revueltos": {},
    }
    return sorted(preparaciones.keys())


def calcular_preparacion_especifica(personas, nombre_preparacion):
    """
    Calcula los ingredientes de una preparación específica.
    
    Args:
        personas (int): Número de personas
        nombre_preparacion (str): Nombre exacto de la preparación
        
    Returns:
        dict: {'preparacion': str, 'ingredientes': dict, 'personas': int} o None si no existe
    
    Ejemplo:
        >>> resultado = calcular_preparacion_especifica(50, "Espaguetis Napolitanos")
    """
    todas_preparaciones = calcular_ingredientes_preparacion(personas)
    
    if nombre_preparacion in todas_preparaciones:
        return {
            'preparacion': nombre_preparacion,
            'personas': personas,
            'ingredientes': todas_preparaciones[nombre_preparacion]
        }
    
    return None


def calcular_refresco(personas):
    """
    Calcula la cantidad de refresco necesaria (8 onzas por persona convertidas a litros).
    
    Args:
        personas (int): Número de personas
        
    Returns:
        float: Cantidad de refresco en litros
    
    Ejemplo:
        >>> refresco = calcular_refresco(50)
        >>> print(f"Necesitas {refresco} litros de refresco")
    """
    # 8 onzas por persona = 236.588 ml (aproximadamente 0.237 litros)
    onzas_por_persona = 8
    ml_por_onza = 29.5735  # 1 onza líquida en ml
    ml_por_persona = onzas_por_persona * ml_por_onza
    litros_por_persona = ml_por_persona / 1000
    
    total_litros = round(personas * litros_por_persona, 2)
    
    return total_litros


def formatear_preparacion_especifica(resultado, formato='texto'):
    """
    Formatea una preparación específica para mostrarla.
    
    Args:
        resultado (dict): Resultado de calcular_preparacion_especifica()
        formato (str): 'texto', 'markdown', 'html' o 'lista'
        
    Returns:
        str o list: Resultado formateado
    """
    if not resultado:
        return "Preparación no encontrada"
    
    preparacion = resultado['preparacion']
    personas = resultado['personas']
    ingredientes = resultado['ingredientes']
    
    if formato == 'lista':
        lista = []
        for ingrediente, cantidad in ingredientes.items():
            # Detectar unidad
            if ingrediente == "Huevos":
                unidad = "unidades"
            elif "Agua" in ingrediente or "Vinagre" in ingrediente:
                unidad = "litros"
            else:
                unidad = "kg"
            
            lista.append({
                'preparacion': preparacion,
                'ingrediente': ingrediente,
                'cantidad': cantidad,
                'unidad': unidad
            })
        return lista
    
    lineas = []
    
    if formato == 'markdown':
        lineas.append(f"**🍳 {preparacion.upper()} - {personas} PERSONAS**\n")
    elif formato == 'html':
        lineas.append(f"<b>🍳 {preparacion.upper()} - {personas} PERSONAS</b>\n")
    else:
        lineas.append(f"🍳 {preparacion.upper()} - {personas} PERSONAS\n")
    
    for ingrediente, cantidad in sorted(ingredientes.items()):
        # Detectar unidad apropiada
        if ingrediente == "Huevos":
            unidad = "unidades"
        elif "Agua" in ingrediente or "Vinagre" in ingrediente:
            unidad = "litros"
        else:
            unidad = "kg"
        
        if formato == 'markdown':
            lineas.append(f"  • **{ingrediente}:** {cantidad} {unidad}")
        else:
            lineas.append(f"  • {ingrediente}: {cantidad} {unidad}")
    
    return '\n'.join(lineas)


def calcular_ingredientes_preparacion(personas):
    """
    Calcula los ingredientes necesarios para las preparaciones básicas.
    
    Args:
        personas (int): Número de personas
        
    Returns:
        dict: Diccionario con preparaciones y sus ingredientes con cantidades
    
    Ejemplo:
        >>> ingredientes = calcular_ingredientes_preparacion(50)
        >>> print(ingredientes['Arroz blanco'])
    """
    
    preparaciones = {
        "Arroz blanco": {
            "Arroz": 100 * personas / 1000,  # kg
            "Agua": 200 * personas / 1000,  # litros (2:1 agua/arroz)
            "Aceite": 5 * personas / 1000,  # kg
            "Sal": 2 * personas / 1000,  # kg
        },
        "Arroz moro": {
            "Arroz crudo": 52 * personas / 1000,  # kg
            "Frijol seco": 26 * personas / 1000,  # kg
            "Agua": 150 * personas / 1000,  # litros
            "Aceite": 3 * personas / 1000,  # kg
            "Cebolla": 10 * personas / 1000,  # kg
            "Ajo": 2 * personas / 1000,  # kg
            "Pimiento": 5 * personas / 1000,  # kg
            "Sal": 1.5 * personas / 1000,  # kg
        },
        "Frijoles negros": {
            "Frijoles (secos)": 45 * personas / 1000,  # kg
            "Agua": 180 * personas / 1000,  # litros (4:1 agua/frijoles)
            "Aceite": 3 * personas / 1000,  # kg
            "Cebolla": 15 * personas / 1000,  # kg
            "Ajo": 3 * personas / 1000,  # kg
            "Pimiento": 10 * personas / 1000,  # kg
            "Sal": 2 * personas / 1000,  # kg
            "Comino": 0.5 * personas / 1000,  # kg
        },
        "Pollo frito": {
            "Pollo (crudo)": 250 * personas / 1000,  # kg
            "Aceite para freír": 50 * personas / 1000,  # kg
            "Sal": 2 * personas / 1000,  # kg
            "Ajo": 2 * personas / 1000,  # kg
            "Limón": 10 * personas / 1000,  # kg
        },
        "Picadillo": {
            "Carne molida": 100 * personas / 1000,  # kg
            "Aceite": 5 * personas / 1000,  # kg
            "Cebolla": 20 * personas / 1000,  # kg
            "Ajo": 3 * personas / 1000,  # kg
            "Pimiento": 15 * personas / 1000,  # kg
            "Tomate": 30 * personas / 1000,  # kg
            "Sal": 1.5 * personas / 1000,  # kg
            "Comino": 0.5 * personas / 1000,  # kg
        },
        "Espaguetis Napolitanos": {
            "Espaguetis (secos)": 75 * personas / 1000,  # kg
            "Agua": 150 * personas / 1000,  # litros
            "Salsa de tomate": 40 * personas / 1000,  # kg
            "Aceite": 5 * personas / 1000,  # kg
            "Cebolla": 15 * personas / 1000,  # kg
            "Ajo": 2 * personas / 1000,  # kg
            "Sal": 2 * personas / 1000,  # kg
            "Queso rallado": 58 * personas / 1000,  # kg (para servir)
        },
        "Plátanos maduros fritos": {
            "Plátano maduro": 150 * personas / 1000,  # kg
            "Aceite para freír": 30 * personas / 1000,  # kg
            "Sal (opcional)": 0.5 * personas / 1000,  # kg
        },
        "Viandas hervidas (Papa/Yuca/Boniato)": {
            "Vianda (papa/yuca/boniato)": 150 * personas / 1000,  # kg
            "Agua": 200 * personas / 1000,  # litros
            "Sal": 2 * personas / 1000,  # kg
        },
        "Ensalada de col": {
            "Col": 150 * personas / 1000,  # kg
            "Tomate": 50 * personas / 1000,  # kg
            "Cebolla": 20 * personas / 1000,  # kg
            "Aceite": 5 * personas / 1000,  # kg
            "Vinagre": 3 * personas / 1000,  # litros
            "Sal": 1 * personas / 1000,  # kg
        },
        "Huevos revueltos": {
            "Huevos": 1.5 * personas,  # unidades
            "Aceite": 3 * personas / 1000,  # kg
            "Cebolla": 10 * personas / 1000,  # kg
            "Sal": 1 * personas / 1000,  # kg
        },
    }
    
    # Redondear valores
    for preparacion in preparaciones:
        for ingrediente in preparaciones[preparacion]:
            valor = preparaciones[preparacion][ingrediente]
            preparaciones[preparacion][ingrediente] = round(valor, 3)
    
    return preparaciones


def formatear_ingredientes_preparacion(preparaciones, formato='texto'):
    """
    Formatea los ingredientes de las preparaciones.
    
    Args:
        preparaciones (dict): Resultado de calcular_ingredientes_preparacion()
        formato (str): 'texto', 'markdown', 'html' o 'lista'
        
    Returns:
        str o list: Ingredientes formateados
    """
    
    if formato == 'lista':
        lista = []
        for preparacion, ingredientes in preparaciones.items():
            for ingrediente, cantidad in ingredientes.items():
                # Detectar unidad
                if ingrediente == "Huevos":
                    unidad = "unidades"
                elif "Agua" in ingrediente or "Vinagre" in ingrediente:
                    unidad = "litros"
                else:
                    unidad = "kg"
                
                lista.append({
                    'preparacion': preparacion,
                    'ingrediente': ingrediente,
                    'cantidad': cantidad,
                    'unidad': unidad
                })
        return lista
    
    lineas = []
    
    if formato == 'markdown':
        lineas.append("**👨‍🍳 INGREDIENTES POR PREPARACIÓN**\n")
    elif formato == 'html':
        lineas.append("<b>👨‍🍳 INGREDIENTES POR PREPARACIÓN</b>\n")
    else:
        lineas.append("👨‍🍳 INGREDIENTES POR PREPARACIÓN\n")
    
    for preparacion, ingredientes in sorted(preparaciones.items()):
        if formato == 'markdown':
            lineas.append(f"\n**{preparacion}:**")
        elif formato == 'html':
            lineas.append(f"\n<b>{preparacion}:</b>")
        else:
            lineas.append(f"\n{preparacion}:")
        
        for ingrediente, cantidad in sorted(ingredientes.items()):
            # Detectar unidad apropiada
            if ingrediente == "Huevos":
                unidad = "unidades"
            elif "Agua" in ingrediente or "Vinagre" in ingrediente:
                unidad = "litros"
            else:
                unidad = "kg"
            
            lineas.append(f"  • {ingrediente}: {cantidad} {unidad}")
    
    return '\n'.join(lineas)


# Ejemplo de uso directo
if __name__ == "__main__":
    # Ejemplo 1: Calcular para 50 personas
    print("=== EJEMPLO 1: Cálculo básico ===")
    resultado = calcular_cantidades_comida(50)
    print(formatear_resultados(resultado))
    
    # Ejemplo 2: Formato markdown (para Telegram)
    print("\n\n=== EJEMPLO 2: Formato Markdown ===")
    print(formatear_resultados(resultado, formato='markdown'))
    
    # Ejemplo 3: Obtener producto específico
    print("\n\n=== EJEMPLO 3: Producto específico ===")
    arroz = obtener_producto_especifico(50, "Arroz blanco")
    print(f"Para 50 personas necesitas: {arroz['cantidad']} {arroz['unidad']} de {arroz['producto']}")
    
    # Ejemplo 4: Lista de productos
    print("\n\n=== EJEMPLO 4: Formato lista (para JSON/API) ===")
    resultado_lista = calcular_cantidades_comida(20)
    lista = formatear_resultados(resultado_lista, formato='lista')
    print(f"Total de productos: {len(lista)}")
    print("Primeros 3 productos:")
    for item in lista[:3]:
        print(f"  {item}")
    
    # Ejemplo 5: Ingredientes para preparaciones
    print("\n\n=== EJEMPLO 5: Ingredientes para preparaciones ===")
    ingredientes = calcular_ingredientes_preparacion(50)
    print(formatear_ingredientes_preparacion(ingredientes))
    
    # Ejemplo 6: Ingredientes formato markdown
    print("\n\n=== EJEMPLO 6: Ingredientes Markdown ===")
    print(formatear_ingredientes_preparacion(ingredientes, formato='markdown'))