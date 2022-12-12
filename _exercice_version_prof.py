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
	return [sample for samples in zip(*channels) for sample in samples]

def separate_channels(samples, num_channels):
	# Faire l'inverse de la fonction merge_channels
	# Si on a en entrée [11, 21, 12, 22, 13, 23]
	# Sur deux channels on obtiendrait :
	# [
	#   [11, 12, 13]
	#   [21, 22, 23]
	# ]
	return [samples[i::num_channels] for i in range(num_channels)]

def sine_gen(freq, amplitude, duration_seconds):
	# Générer une onde sinusoïdale à partir de la fréquence et de l'amplitude donnée, sur le temps demandé et considérant le taux d'échantillonnage.
	# Les échantillons sont des nombres réels entre -1 et 1.
	for i in range(int(SAMPLING_FREQ * duration_seconds)):
		# Formule de la valeur y d'une onde sinusoïdale à l'angle x en fonction de sa fréquence F et de son amplitude A :
		# y = A * sin(F * x), où x est en radian.
		# Si on veut le x qui correspond au moment t, on peut dire que 2π représente une seconde, donc x = t * 2π,
		# Or t est en secondes, donc t = i / nb_échantillons_par_secondes, où i est le numéro d'échantillon.
		yield amplitude * math.sin(freq * (i / SAMPLING_FREQ * 2*math.pi))

def convert_to_bytes(samples):
	# Convertir les échantillons en tableau de bytes en les convertissant en entiers 16 bits.
	# Les échantillons en entrée sont entre -1 et 1, nous voulons les mettre entre -MAX_SAMPLE_VALUE et MAX_SAMPLE_VALUE
	packer = struct.Struct("h")
	data = bytes()
	for sample in samples:
		integer_sample = int(sample * MAX_SAMPLE_VALUE)
		encoded_sample = packer.pack(integer_sample)
		data += encoded_sample
	return data

def convert_to_samples(bytes):
	# Faire l'opération inverse de convert_to_bytes, en convertissant des échantillons entier 16 bits en échantillons réels
	unpacker = struct.Struct("h")
	samples = []
	for i in range(0, len(bytes), 2):
		encoded_sample = bytes[i:i+2]
		integer_sample = unpacker.unpack(encoded_sample)[0]
		sample = integer_sample / MAX_SAMPLE_VALUE
		samples.append(sample)
	return samples


def main():
	print([int(b) for b in struct.pack("h", 258)])
	print(struct.unpack("hhh", bytes([2, 1, 42, 0, 0, 1])))

	print(merge_channels([[11, 12], [21, 22]]))
	print(separate_channels([11, 12, 21, 22, 31, 32], 3))

	if not os.path.exists("output"):
		os.mkdir("output")

	with wave.open("output/perfect_fifth.wav", "wb") as writer:
		writer.setnchannels(2)
		writer.setsampwidth(2)
		writer.setframerate(SAMPLING_FREQ)

		# On génére un la3 (220 Hz) et un mi4 (intonnation juste, donc ratio de 3/2)
		samples1 = [s for s in sine_gen(220, 0.4, 3.0)]
		samples2 = [s for s in sine_gen(220 * (3/2), 0.3, 3.0)]

		# On met les samples dans des channels séparés (la à gauche, mi à droite)
		merged = merge_channels([samples1, samples2])
		data = convert_to_bytes(merged)

		writer.writeframes(data)

	with wave.open("data/stravinsky.wav", "rb") as reader:
		data = reader.readframes(int(reader.getnframes() * 0.2))
		samples = convert_to_samples(data)
		# On réduit le volume (on pourrait faire n'importe quoi avec les samples à ce stade.
		samples = [s * 0.2 for s in samples]
		data = convert_to_bytes(samples)
		with wave.open("output/stravinsky_mod.wav", "wb") as writer:
			writer.setnchannels(2)
			writer.setsampwidth(2)
			writer.setframerate(SAMPLING_FREQ)
			writer.writeframes(data)



if __name__ == "__main__":
	main()
