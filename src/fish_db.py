"""
Pesca App - Fish Species Database
Pesca recreativa en México y costa oeste USA
"""

# Base de datos de especies de pesca deportiva
FISH_SPECIES = {
    # ========== PECADOS GRANDES (Big Game) ==========
    "dorado": {
        "name": "Dorado",
        "scientific": "Coryphaena hippurus",
        "family": "Coryphaenidae",
        "español": "Delfín/Mahi-mahi",
        "description": " Pez colorido y acrobático. Known for explosive strikes and fights. one of the most popular game fish in tropical waters.",
        "size_range": "20-80 lbs típicamente, hasta 100+ lbs",
        "best_season": "Mayo-Noviembre (agua tibia)",
        "water_temp": "22-30°C",
        "best_time": "Amanecer y atardecer",
        "techniques": [" trolling", "castaneo", "fly fishing"],
        "lures": ["poppers", "bucktail", "trolled lures", "swimbaits"],
        "baits": ["sardina", "macarela", "calamón"],
        "best_locations": ["La Paz", "Cabo San Lucas", "Mazatlán", "Costa Pacífica"],
        "difficulty": "intermedio",
        "food_value": "Excelente - carne blanca y sabrosa"
    },
    "marlin_negro": {
        "name": "Marlin Negro",
        "scientific": "Makaira indica",
        "family": "Istiophoridae",
        "español": "Black Marlin",
        "description": "El pez más grande del Pacífico. Masivo y extremadamente poderoso. Sueño de todo pescador deportivo.",
        "size_range": "200-1000+ lbs",
        "best_season": "Julio-Octubre",
        "water_temp": "24-28°C",
        "best_time": "Mediodía (agua profunda)",
        "techniques": ["trolling pesado", "deep dropping"],
        "lures": ["marlin lures grandes", "squid", "mullet"],
        "baits": ["marlin bait", "calamón grande", "bonito"],
        "best_locations": ["Cabo San Lucas", "Puerto Los Cabos", "Revillagigedo"],
        "difficulty": "avanzado",
        "food_value": "Carne textura firme"
    },
    "marlin_azul": {
        "name": "Marlin Azul",
        "scientific": "Makaira nigricans",
        "family": "Istiophoridae",
        "español": "Blue Marlin",
        "description": "Gran pez de mar. Muito acrobático en la lucha. Una experiencia de pesca inolvidable.",
        "size_range": "150-800 lbs",
        "best_season": "Junio-Noviembre",
        "water_temp": "22-28°C",
        "best_time": "Mañana temprano",
        "techniques": ["trolling", "circle hook"],
        "lures": ["blue marlin lures", "squid", "baitfeeder"],
        "baits": ["sailor's choice", "ballyhoo", "mackerel"],
        "best_locations": ["Cabo San Lucas", "Costa Rica", "Hawaii"],
        "difficulty": "avanzado",
        "food_value": "Excelente para sushi"
    },
    "sailfish": {
        "name": "Marl Vela o Pez Vela",
        "scientific": "Istiophorus platypterus",
        "family": "Istiophoridae",
        "español": "Sailfish",
        "description": "Known por su vela dorsal distintiva y saltos acrobático. MuyPopular en tournaments.",
        "size_range": "40-100 lbs",
        "best_season": "Diciembre-Abril",
        "water_temp": "21-26°C",
        "best_time": "Mañana",
        "techniques": ["trolling", "kite fishing", "live bait"],
        "baits": ["sardina", "anchoveta", "mackerel"],
        "best_locations": ["Costa Rica", "Guatemala", "La Paz"],
        "difficulty": "intermedio",
        "food_value": "Very good"
    },
    
    # ========== PECADOS DE ROCA Y FONDO ==========
    "cabrilla": {
        "name": "Cabrilla",
        "scientific": "Sebastes spp.",
        "family": "Sebastidae",
        "español": "Rockfish/Red Rockfish",
        "description": "Pez de roca muito popular. Excelente para mesa. Varias espécies con names diferentes.",
        "size_range": "1-10 lbs",
        "best_season": "Todo el año",
        "water_temp": "13-18°C",
        "best_time": "Cualquier hora",
        "techniques": ["fondo", "drifting", "spearfishing"],
        "lures": ["rebel", "krocodile"],
        "baits": ["sardina", "calamón", "mussels", "cangrejo"],
        "best_locations": ["Ensenada", "San Felipe", "BC"],
        "difficulty": "principiante",
        "food_value": "Excelente - muy sabroso"
    },
    "lubina": {
        "name": "Lubina",
        "scientific": "Micropterus spp.",
        "family": "Centrarchidae",
        "español": "Bass",
        "description": "Largosta popular en água dulce y salobre. Muy agresivo y divertido depescar.",
        "size_range": "1-5 lbs típicamente",
        "best_season": "Primavera-Otoño",
        "water_temp": "15-25°C",
        "best_time": "Amanecer/Atardecer",
        "techniques": ["castaneo", "topwater", "drop shot"],
        "lures": ["spoons", "swimbaits", "crankbaits", "jigs"],
        "baits": ["gusanos", "ranas", "minnows"],
        "best_locations": ["Lagunas costeras", "Ríos"],
        "difficulty": "principiante",
        "food_value": "Good"
    },
    "pargo": {
        "name": "Pargo",
        "scientific": "Lutjanus spp.",
        "family": "Lutjanidae",
        "español": "Snapper",
        "description": "Grupo de peces de carne blanca y sabor suave. Muy valorado paramesa.",
        "size_range": "1-15 lbs",
        "best_season": "Todo el año, mejor primavera",
        "water_temp": "20-28°C",
        "best_time": "Nocturno/Fondo",
        "techniques": ["fondo", "drifting", "chumming"],
        "baits": ["sardina", "calamón", "calamari", "cangrejo"],
        "best_locations": ["Mazatlán", "Cabo", "Manzanillo"],
        "difficulty": "principiante",
        "food_value": "Excelente"
    },
    "huachinango": {
        "name": "Huachinango",
        "scientific": "Lutjanus peru",
        "family": "Lutjanidae",
        "español": "Pacific Red Snapper",
        "description": "El pargo rojo del Pacífico. Icono de la pesca mexicana. Delicioso.",
        "size_range": "3-30 lbs",
        "best_season": "Todo el año",
        "water_temp": "18-26°C",
        "best_time": "Noche y madrugada",
        "techniques": ["fondo", "drifting", "deep sea"],
        "baits": ["sardina", "calamón", "jibia"],
        "best_locations": ["La Paz", "Cabo", "Mazatlán"],
        "difficulty": "intermedio",
        "food_value": "SUPERIOR - el más valioso"
    },
    
    # ========== PECECILLOS DE CAÑA ==========
    "tuna": {
        "name": "Atún",
        "scientific": "Thunnus spp.",
        "family": "Scombridae",
        "español": "Tuna",
        "description": "Pez de Cardumen. Combates intensos y veloces. highly migratory.",
        "size_range": "20-300+ lbs",
        "best_season": "Primavera-Invierno",
        "water_temp": "15-25°C",
        "best_time": "Cualquier hora",
        "techniques": ["trolling", "casting", "live bait"],
        "lures": ["casting", "poppers", "fly"],
        "baits": ["sardina", "anchoveta", "mackerel"],
        "best_locations": ["Cabo", "Coronto", "Costa Pacífico"],
        "difficulty": "intermedio-avanzado",
        "food_value": "Excelente - sashimi"
    },
    "bonito": {
        "name": "Bonito",
        "scientific": "Sarda spp.",
        "family": "Scombridae",
        "español": "Bonito",
        "description": "Tuna pequeno pero muy agresivo. Excelente para pescar ligero.",
        "size_range": "3-15 lbs",
        "best_season": "Primavera-Otoño",
        "water_temp": "14-22°C",
        "best_time": "Día con cardúmenes",
        "techniques": ["casting", "trolling lightweight", "fly"],
        "lures": ["small lures", "flies", "spoons"],
        "baits": ["sardina", "mackerel"],
        "best_locations": ["BC", "Ensenada", "Cabo"],
        "difficulty": "principiante",
        "food_value": "Good para conserva"
    },
    "wahoo": {
        "name": "Wahoo",
        "scientific": "Acanthocybium solandri",
        "family": "Scombridae",
        "español": "Wahoo",
        "description": "Extremadamente rápido. Conocido por strikes explosive.",
        "size_range": "30-100 lbs",
        "best_season": "Marzo-Junio",
        "water_temp": "24-28°C",
        "best_time": "Mañana",
        "techniques": ["high speed trolling"],
        "lures": ["high speed lures", "squid"],
        "baits": ["ballyhoo", "sardina"],
        "best_locations": ["Cabo San Lucas", "Costa Rica"],
        "difficulty": "avanzado",
        "food_value": "Excelente"
    },
    "mackerel": {
        "name": "Macarela",
        "scientific": "Scomber japonicus",
        "family": "Scombridae",
        "español": "Pacific Mackerel",
        "description": "Pez de cardumen muitoactivo. Excelente como cebo vivo.",
        "size_range": "1-3 lbs",
        "best_season": "Invierno-Primavera",
        "water_temp": "12-18°C",
        "best_time": "Cardúmenes en superficie",
        "techniques": ["casting", "sabiki"],
        "baits": ["sardina", "anchoa"],
        "best_locations": ["BC", "Ensenada"],
        "difficulty": "principiante",
        "food_value": "Good"
    },
    
    # ========== PECES DE AGUA DULCE Y ESTUARIOS ==========
    "trucha": {
        "name": "Trucha",
        "scientific": "Oncorhynchus spp.",
        "family": "Salmonidae",
        "español": "Trout",
        "description": "Pez de agua fría. Muito apreciado por pescadores Fly.",
        "size_range": "0.5-10 lbs",
        "best_season": "Invierno-Primavera",
        "water_temp": "8-15°C",
        "best_time": "Amanecer",
        "techniques": ["fly fishing", "ninfas", "streamers"],
        "lures": ["flies", "spoons", "worms"],
        "baits": ["ninfas", "gusanos", "grillos"],
        "best_locations": ["Sierra de BCS", "Ríos montañas"],
        "difficulty": "intermedio",
        "food_value": "Excelente"
    },
    "bagre": {
        "name": "Bagre Marino",
        "scientific": "Ariopsis spp.",
        "family": "Ariidae",
        "español": "Sea Catfish",
        "description": "Pez de bigotes. Puede picar fuerte. Importante manejar con cuidado por spines.",
        "size_range": "1-5 lbs",
        "best_season": "Todo el año",
        "water_temp": "18-30°C",
        "best_time": "Noche",
        "techniques": ["fondo", "surf fishing"],
        "baits": ["sardina", "calamón", "intestinos"],
        "best_locations": ["Estuarios", "Lagunas"],
        "difficulty": "principiante",
        "food_value": "Regular"
    },
    "robalo": {
        "name": "Robalo",
        "scientific": "Centropomus spp.",
        "family": "Centropomidae",
        "español": "Snook",
        "description": "Pez de manglar. Fuerte y acrobático. Clásico de agua salobre.",
        "size_range": "5-30 lbs",
        "best_season": "Otoño-Invierno",
        "water_temp": "20-28°C",
        "best_time": "Amanecer/Atardecer",
        "techniques": ["live bait", "casting", "topwater"],
        "lures": ["crankbaits", "topwater", "jigs"],
        "baits": ["sardina", "mojarra", "cangrejo"],
        "best_locations": ["Estuarios BCS", "Lagunas"],
        "difficulty": "intermedio",
        "food_value": "Good"
    },
    "mojarra": {
        "name": "Mojarra",
        "scientific": "Gerres spp.",
        "family": "Gerreidae",
        "español": "Mojarra",
        "description": "Pez pequeño muy común. Excelente pesca para principiantes y niños.",
        "size_range": "0.25-2 lbs",
        "best_season": "Todo el año",
        "water_temp": "18-30°C",
        "best_time": "Cualquier hora",
        "techniques": ["micro fishing", "fondo"],
        "baits": ["pan", "gusanos", "masa"],
        "best_locations": ["Estuarios", "Muelles"],
        "difficulty": "muy fácil",
        "food_value": "Regular"
    },
    
    # ========== OTROS ==========
    "tiburon": {
        "name": "Tiburón",
        "scientific": "Carcharhinus spp.",
        "family": "Carcharhinidae",
        "español": "Shark",
        "description": "Varias espécies. Algunos muy buscados por su lucha poderosa.",
        "size_range": "20-300+ lbs",
        "best_season": "Verano-Otoño",
        "water_temp": "18-26°C",
        "best_time": "Noche/Amanecer",
        "techniques": ["surf", "boat", "chumming"],
        "baits": ["fish heads", "señal", "sardina"],
        "best_locations": ["CostaBC", "Cabo"],
        "difficulty": "intermedio",
        "food_value": "Varía por especie"
    },
    "mantarraya": {
        "name": "Mantarraya",
        "scientific": "Manta birostris",
        "family": "Mobulidae",
        "español": "Manta Ray",
        "description": "No es para comer, pero su pesca es-experiencia única. Released siempre.",
        "size_range": "500-2000+ lbs (ancia",
        "best_season": "Verano",
        "water_temp": "22-28°C",
        "best_time": "Limpio",
        "techniques": ["drifting", " Sight fishing"],
        "lures": ["neón para visibilidad"],
        "baits": ["no se usa típicamente"],
        "best_locations": ["La Paz", "Cabo", "Revillagigedo"],
        "difficulty": "avanzado",
        "food_value": "NO sepesca - debe liberarse"
    }
}

# Técnicas de pesca por categoría
FISHING_TECHNIQUES = {
    "casting": {
        "name": "Casting",
        "description": "Lanzar yretrieve señuelo o appoggi",
        "difficulty": "principiante",
        "best_for": ["bass", "trout", "robalo", "bonito"]
    },
    "trolling": {
        "name": "Trolling / Arrastre",
        "description": "Remolcar señuelos desde barca en movimiento",
        "difficulty": "principiante",
        "best_for": ["tuna", "dorado", "marlin", "wahoo"]
    },
    "fondo": {
        "name": "Pesca de Fondo",
        "description": "Sed的一条 en el fondo con cebo",
        "difficulty": "principiante",
        "best_for": ["pargo", "huachinango", "cabrilla", "bagre"]
    },
    "fly_fishing": {
        "name": "Fly Fishing",
        "description": "Mosca artificialce molinete",
        "difficulty": "avanzado",
        "best_for": ["trout", "bass", "robalo"]
    },
    "spearfishing": {
        "name": "Pesca con Arpón",
        "description": "Buceo yarpón subacuático",
        "difficulty": "avanzado",
        "best_for": ["pargo", "cabrilla", "lubina"]
    },
    "surf_fishing": {
        "name": "Surf Casting",
        "description": "Pesca desde lama desde la orilla",
        "difficulty": "intermedio",
        "best_for": ["tiburón", "corbina", "bagre"]
    },
    "jigging": {
        "name": "Jigging",
        "description": "Subir ybajar jig verticalmente",
        "difficulty": "intermedio",
        "best_for": ["pargo", "huachinango", "cabrilla"]
    }
}

# señuelos populars
LURES = {
    "popper": {"name": "Popper", "best_for": ["dorado", "bass", "robalo"]},
    "crankbait": {"name": "Crankbait", "best_for": ["bass", "trout", "robalo"]},
    "spoon": {"name": "Cuchara/Spoon", "best_for": ["trout", "bonito", "cabrilla"]},
    "swimbait": {"name": "Swimbait", "best_for": ["dorado", "bass", "trout"]},
    "jig": {"name": "Jig", "best_for": ["bass", "trout", "pargo"]},
    "worm": {"name": "Gusano artificial", "best_for": ["bass", "trout"]},
    "fly": {"name": "Mosca", "best_for": ["trout", "bass"]},
    "bucktail": {"name": "Bucktail", "best_for": ["dorado", "cabrilla"]}
}

# Carnadas naturals
BAITS = {
    "sardina": {"name": "Sardina", "type": "fresca", "best_for": ["dorado", "tuna", "pargo", "huachinango"]},
    "calamon": {"name": "Calambel/Colisa", "type": "fresco", "best_for": ["pargo", "huachinango", "cabrilla"]},
    "anchoveta": {"name": "Anchoveta", "type": "fresca/salada", "best_for": ["tuna", "bonito", "marlin"]},
    "macarela": {"name": "Macarela", "type": "fresca", "best_for": ["dorado", "tuna", "marlin"]},
    "cangrejo": {"name": "Cangrejo", "type": "vivo", "best_for": ["pargo", "cabrilla", "robalo"]},
    "gusano": {"name": "Gusanos", "type": "vivo", "best_for": ["trout", "bass", "mojarra"]},
    "rana": {"name": "Rana", "type": "vivo", "best_for": ["bass", "trout"]},
    "masa": {"name": "Masa/Pasta", "type": "artificial", "best_for": ["mojarra", "bagre"]}
}

# Recomendaciones por condición
def get_recommendations(fishing_score, weather, tides):
    """Genera recomendaciones basadas en condiciones"""
    recs = []
    
    if fishing_score >= 8:
        recs.append({
            "type": "excelente",
            "message": "¡Día excellent para pesca! Condiciones óptimas."
        })
    elif fishing_score >= 5:
        recs.append({
            "type": "bueno",
            "message": "Día correcto para pescar. Buenos resultados esperados."
        })
    else:
        recs.append({
            "type": "regular",
            "message": "Condiciones no ideales. Considera otro día o cambia técnica."
        })
    
    # Por marea
    if tides.get("is_incoming"):
        recs.append({
            "type": "marea",
            "message": "MareaSubiendo - peces más activosFA enfoque."
        })
    
    # Por temperatura
    temp = weather.get("temperature", 20)
    if temp < 15:
        recs.append({
            "type": "temperatura",
            "message": "Agua fría - pesca a fondoopec depths."
        })
    elif temp > 28:
        recs.append({
            "type": "temperatura",
            "message": "Agua trèscaliente - pesca temprano o atardecer."
        })
    
    return recs