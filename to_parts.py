# Разделить результат скрипта Synonym на X равных частей


import csv
import random

links_file = 'files/links_v2.csv'
input_file = 'files/b3 fix_result.txt'
text_to_replace = ''
parts = 4


def main():
	links = []
	with open(links_file) as f:
		for line in csv.reader(f):
			links.extend(line)

	phrases = []
	with open(input_file) as f:
		for line in f.readlines():
			phrases.append(line)

	part_size = len(phrases) / parts
	for i in range(parts):
		output_file = f'{input_file.replace(".txt", "")}_pt{str(i+1)}.txt'
		links_part = links[int((len(links)/parts)*i) : int((len(links)/parts)*(i+1))]
		with open(output_file, 'w') as f:
			for phrase in phrases[int(part_size*i) : int(part_size*(i+1))]:
				if text_to_replace:
					phrase = phrase.replace(text_to_replace, random.choice(links_part))
				f.write(phrase)


if __name__ == '__main__':
	main()