#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import wave
import struct
import math


SAMPLING_FREQ = 44100 # Hertz, taux d'échantillonnage standard des CD
SAMPLE_WIDTH = 16 # Échantillons de 16 bit
MAX_SAMPLE_VALUE = 2**(SAMPLE_WIDTH-1) - 1


def merge_channels(channels):
	# À partir de plusieurs listes d'échantillons (réels), les combiner de façon à ce que la liste retournée aie la forme :
	# [c[0][0], c[1][0], c[2][0], c[0][1], c[1][1], c[2][1], ...] où c est l'agument channels
	pass

def separate_channels(samples, num_channels):
	# Faire l'inverse de la fonction merge_channels
	pass

def sine_gen(freq, amplitude, duration_seconds):
	# Générer une onde sinusoïdale à partir de la fréquence et de l'amplitude donnée, sur le temps demandé et considérant le taux d'échantillonnage.
	# Les échantillons sont des nombres réels entre -1 et 1.
	pass

def convert_to_bytes(samples):
	# Convertir les échantillons en tableau de bytes en les convertissant en entiers 16 bits.
	# Les échantillons en entrée sont entre -1 et 1, nous voulons les mettre entre -MAX_SAMPLE_VALUE et MAX_SAMPLE_VALUE
	pass

def convert_to_samples(bytes):
	# Faire l'opération inverse de convert_to_bytes, en convertissant des échantillons entier 16 bits en échantillons réels
	pass


def main():
	if not os.path.exists("output"):
		os.mkdir("output")

	print(separate_channels([[11, 12], [21, 22], [31, 32]], 3))

	with wave.open("output/perfect_fifth.wav", "wb") as writer:
		writer.setnchannels(2)
		writer.setsampwidth(2)
		writer.setframerate(SAMPLING_FREQ)
		writer.setnframes(SAMPLING_FREQ*5)

		# On générè un la3 (220 Hz) et un mi4 (intonnation juste, donc ratio de 3/2)
		samples1 = [s for s in sine_gen(220, 0.4, 3.0)]
		samples2 = [s for s in sine_gen(220 * (3/2), 0.3, 3.0)]

		# On met les samples dans des channels séparés (la à gauche, mi à droite)
		merged = merge_channels([samples1, samples2])
		data = convert_to_bytes(merged)

		writer.writeframes(data)

if __name__ == "__main__":
	main()
