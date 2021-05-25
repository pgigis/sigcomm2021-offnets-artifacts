import os
import json
import pytricia

# Load the IP-to-AS mapping file
def load_ip_to_as_mapping(filename):
	pyt = pytricia.PyTricia()
	try:
		with open(filename, 'rt') as f:
			data = json.load(f)
		for prefix in data:
			pyt[prefix] = data[prefix]
	except:
		print("Couldn't load/process IP-to-AS mapping file \"{}\"".format(filename))
		return None
	return pyt


# Create path
def createPath(path):
	if not os.path.exists(path):
		os.makedirs(path)


# Load and the config file
def load_config_file(configFile):
	hg_keyword_to_hg_ases_key = dict()
	try:
		with open(configFile, 'rt') as f:
			for line in f:
				data = json.loads(line.rstrip())
				hg_keyword_to_hg_ases_key[data['hypergiant-keyword']] = data['hypergiant-ases-key']
	except:
		print("Couldn't load/process config file \"{}\"".format(configFile))
		return None
	return hg_keyword_to_hg_ases_key


def load_hypergiant_ases(filename):
	hg_ases = dict()
	try: 
		with open(filename, 'rt') as f:
			data = json.load(f)
			for hypergiant in data:
					hg_ases[hypergiant] = data[hypergiant]['asns']
	except:
		print("Couldn't load \"{}\".".format(filePath))
		return None

	return hg_ases