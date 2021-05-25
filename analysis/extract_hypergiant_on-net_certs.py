import os
import json
import pprint
import argparse
import pytricia


# Load the IP-to-AS mapping file
def load_ip_to_as_mapping(filename):
	pyt = pytricia.PyTricia()
	with open(filename, 'rt') as f:
		data = json.load(f)
	for prefix in data:
		pyt[prefix] = data[prefix]
	return pyt


def load_hypergiant_ases(date, folderPath="../datasets/hypergiants/"):
	month, year = date.split('-')
	hg_asn_to_hg_keyword = dict()
	hg_keywords_available = set()
	filePath = folderPath + year + "_" + month + "_hypergiants_asns.json"
	try: 
		with open(filePath, 'rt') as f:
			data = json.load(f)
			for hypergiant in data:
				for AS in data[hypergiant]['asns']:
					hg_asn_to_hg_keyword[int(AS)] = hypergiant
					hg_keywords_available.add(hypergiant)
	except:
		print("Couldn't load \"{}\".".format(filePath))
		exit()
	return hg_asn_to_hg_keyword, hg_keywords_available


def load_config_file(configFile):
	hg_keyword_to_ases_key = dict()
	try:
		with open(configFile, 'rt') as f:
			for line in f:
				data = json.loads(line.rstrip())
				hg_keyword_to_ases_key[data['hypergiant-keyword']] = data['hypergiant-ases-key']
	except:
		print("Couldn't load/process config file \"{}\"".format(configFile))
		exit()
	return hg_keyword_to_ases_key


def proces_configuration_file(configuration_input, hg_asn_to_hg_keyword, hg_keywords_available):
	# Check if for all keywords, a hypergiant-ases-key exist.
	invalid = False
	for hg_key in hg_asn_to_hg_keyword:
		if hg_asn_to_hg_keyword[hg_key] not in hg_keywords_available:
			print("hypergiant-ases-key \"{}\" not found.".format(hg_asn_to_hg_keyword[hg_key]))
			invalid = True

	if invalid == True:
		print("Available \"hypergiant-ases-key\" keys:\n{}".format(hg_keywords_available))
		exit() 

	hg_asn_to_hg_keywords = dict()
	all_hg_keywords = set()
	
	for hg_asn in hg_asn_to_hg_keyword:
		for keyword in configuration_input:
			if hg_asn_to_hg_keyword[hg_asn] == configuration_input[keyword]:
				if hg_asn not in hg_asn_to_hg_keywords:
					hg_asn_to_hg_keywords[hg_asn] = set()
				hg_asn_to_hg_keywords[hg_asn].add(keyword)
				all_hg_keywords.add(keyword)
	
	return hg_asn_to_hg_keywords, all_hg_keywords


def createFilePaths(filePathToStoreResults):
	if not os.path.exists(filePathToStoreResults):
		os.makedirs(filePathToStoreResults)


def process_ee_certs(inputFile, ip_to_as, hg_asn_to_hg_keywords, all_hg_keywords, filePathToStoreResults):
	openFiles_l = dict()

	for hg_keyword in all_hg_keywords:
		filePath = filePathToStoreResults + hg_keyword + ".txt"
		openFiles_l[hg_keyword] = open(filePath, 'wt')


	with open(inputFile, 'rt') as f:
		for line in f:
			data = json.loads(line)

			for ip in data:
				asns = list()
				try:
					asns = ip_to_as[ip]
				except:
					pass
			
			keywords_matched = None
			foundASN = None
			# Iterate over all ASNs of the IP-to-AS mapping (MOAS)
			for asn in asns:
				# Check if the ASN match to any of the hypergiant ASes
				if asn in hg_asn_to_hg_keywords: 
					keywords_matched = hg_asn_to_hg_keywords[asn]
					foundASN = asn
					break

			if keywords_matched is not None:
				if 'subject' in data[ip]:
					if 'organization' in data[ip]['subject']:
						organization_value = " ".join(data[ip]['subject']['organization'])
						for keyword in keywords_matched:
							if keyword in organization_value.lower():
								storeJSON = { 
												"ip" : ip,
												"ASN" : foundASN,
												"dns_names" : data[ip]['dns_names'],
												"subject:organization" : organization_value
											}
								openFiles_l[keyword].write("{}\n".format(json.dumps(storeJSON)))	

	for file in openFiles_l:
		openFiles_l[file].close()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process hypergiant on-net certificates.')
	parser.add_argument('-d', '--date',
						help='Date of snapshot to parse. Date format: YYYY-MM',
						type=str,
						required=True)
	parser.add_argument('-i', '--inputFile',
						type=str,
						help="The path to the input certificate.",
						required=True)
	parser.add_argument('-c', '--configFile',
						type=str,
						help="The path of the configuration file.",
						required=True)
	parser.add_argument('-a', '--ipToASFile',
						type=str,
						help="The path of the IP-to-AS file.",
						required=True)

	args = parser.parse_args()

	filePathToStoreResults = "/".join(args.inputFile.split("/")[:-1]) + "/on-nets/"
	createFilePaths(filePathToStoreResults)

	ip_to_as = load_ip_to_as_mapping(args.ipToASFile)

	hg_asn_to_hg_keyword, hg_keywords_available = load_hypergiant_ases(args.date)
	configuration_input = load_config_file(args.configFile)

	hg_asn_to_hg_keywords, all_hg_keywords = proces_configuration_file(configuration_input, hg_asn_to_hg_keyword, hg_keywords_available)
	
	process_ee_certs(args.inputFile, ip_to_as, hg_asn_to_hg_keywords, all_hg_keywords, filePathToStoreResults)





