def calcular_prioridad(impacto_academico, personas_afectadas, minutos_espera):

    puntaje = impacto_academico + personas_afectadas

    puntos_espera = minutos_espera // 60

    puntaje += puntos_espera

    if puntaje > 10:
        puntaje = 10

    if puntaje >= 8:
        return "ALTA"
    elif puntaje >= 5:
        return "MEDIA"
    else:
        return "BAJA"