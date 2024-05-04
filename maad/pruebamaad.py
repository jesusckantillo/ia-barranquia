import numpy as np
import matplotlib.pyplot as plt
from maad import sound, util

audio_file = "botbueno.wav"
s, fs = sound.load(audio_file) 
Sxx, tn, fn, ext = sound.spectrogram(s,fs)
util.plot_spectrogram(Sxx, ext, db_range=50, gain=40, figsize=(4,10))

plt.show()


