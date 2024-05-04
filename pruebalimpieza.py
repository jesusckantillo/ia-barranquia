import parselmouth

snd = parselmouth.Sound("xd.wav")

# Definir umbral de amplitud para considerar como silencio
umbral_amplitud = 0.05  # Puedes ajustar este valor según tus necesidades

# Identificar los segmentos de silencio basados en el umbral de amplitud
segmentos_silencio = []
in_silence = False
inicio_silencio = 0

for i, valor_amplitud in enumerate(snd.values.T):
    if not in_silence and abs(valor_amplitud) < umbral_amplitud:
        in_silence = True
        inicio_silencio = snd.xs()[i]
    elif in_silence and abs(valor_amplitud) >= umbral_amplitud:
        in_silence = False
        segmentos_silencio.append((inicio_silencio, snd.xs()[i]))

# Eliminar segmentos de silencio
for inicio, fin in segmentos_silencio:
    snd = snd.without_range(inicio, fin)

# Guardar el audio limpio
snd.save("xdlimpio.wav", "WAV")
