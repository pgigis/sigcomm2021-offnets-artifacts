import os
import json
import socket
import pprint
import argparse
import pytricia

from anytree import Node


# Load the IP-to-AS mapping file
def load_ip_to_as_mapping(filename):
	pyt = pytricia.PyTricia()
	with open(filename, 'rt') as f:
		data = json.load(f)
	for prefix in data:
		pyt[prefix] = data[prefix]
	return pyt


def load_tld_suffixes(file_path_suffixes="../datasets/tld_suffixes/suffixes.txt"):
	suffixes = dict()
	with open(file_path_suffixes, 'rt') as f:
		for line in f:
			if "!" in line or "//" in line:
				continue
			if line[0] == "*":
				suffixes[line[2:].rstrip()] = None
			else:
				suffixes[line.rstrip()] = None
	return suffixes


def is_hostname(dns_name):
	try:
		socket.inet_aton(dns_name)
		return False
	except socket.error as e:
		return True


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


def createFilePaths(filePathToStoreResults):
	if not os.path.exists(filePathToStoreResults):
		os.makedirs(filePathToStoreResults)


def calc_TLD_plus_one(dns_name, suffixes):
	dns_name = dns_name.lstrip('*.')

	if '/' in dns_name:
		dns_name = dns_name.replace('/', '')

	# If not a valid dns_name skip it
	if '.' not in dns_name:
		return None, None

	# Split domain name to parts
	domain_name_fragmented = dns_name.split('.')
	# Construct TLD+1 key (e.g '.google.com' -> 'com.google')
	tld_plus_one = domain_name_fragmented[-1] + '.' + domain_name_fragmented[-2]

	tld_plus_one_check_suffix = domain_name_fragmented[-2] + '.' + domain_name_fragmented[-1]

	if tld_plus_one_check_suffix in suffixes:
		if len(domain_name_fragmented) > 3:
			tld_plus_one = domain_name_fragmented[-1] + '.' + domain_name_fragmented[-2] + '.' + domain_name_fragmented[-3]
			domain_name_fragmented[-2] = domain_name_fragmented[-1] + '.' + domain_name_fragmented[-2]
			del domain_name_fragmented[-1]

	return tld_plus_one, domain_name_fragmented



def generate_on_net_fingerprints(on_net_folder, suffixes):
	files = os.listdir(on_net_folder)
	dns_names_per_hg = dict()
	if on_net_folder[-1] != '/':
		on_net_folder += '/'
	for file in files:
		if '.txt' in file:
			hg_keyword = file.split('.')[0]
			if  hg_keyword not in dns_names_per_hg:
				dns_names_per_hg[hg_keyword] = dict()

			with open(on_net_folder + file, 'rt') as f:
				for line in f:
					data = json.loads(line)
					if 'dns_names' in data:
						for dns_name in data['dns_names']:
							if is_hostname(dns_name):
							# Exclude cases where dns_name is not a hostname but an IP
								tld_plus_one, domain_name_fragmented = calc_TLD_plus_one(dns_name, suffixes)
								dns_names_per_hg[hg_keyword][tld_plus_one] = None
	return dns_names_per_hg


def process_off_nets(inputFile, ip_to_as, dns_names_per_hg, hg_asn_to_hg_keyword, tld_suffixes, filePathToStoreResults):
	hg_keywords = dns_names_per_hg.keys()

	openFiles_l = dict()

	for hg_keyword in hg_keywords:
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

			is_on_net = False

			# Iterate over all ASNs of the IP-to-AS mapping (MOAS)
			for asn in asns:
				# Check if the ASN match to any of the hypergiant ASes
				if asn in hg_asn_to_hg_keyword: 
					is_on_net = True

			if is_on_net == False:
				if 'subject' in data[ip]:
					if 'organization' in data[ip]['subject']:
						organization_value = (" ".join(data[ip]['subject']['organization'])).lower()
						for hg_keyword in hg_keywords:
							if hg_keyword in organization_value:
								for dns_name in data[ip]['dns_names']:
									allDNS_names_match = True
									tld_plus_one, domain_name_fragmented = calc_TLD_plus_one(dns_name, tld_suffixes)
									if tld_plus_one not in dns_names_per_hg[hg_keyword]:
										allDNS_names_match = False

								if allDNS_names_match == True:
									storeJSON = { 
												"ip" : ip,
												"ASN" : asns[0],
												"dns_names" : data[ip]['dns_names'],
												"subject:organization" : organization_value
												}
									openFiles_l[hg_keyword].write("{}\n".format(json.dumps(storeJSON)))
	for file in openFiles_l:
		openFiles_l[file].close()




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process hypergiant off-net certificates.')
	parser.add_argument('-d', '--date',
						help='Date of snapshot to parse. Date format: YYYY-MM',
						type=str,
						required=True)
	parser.add_argument('-i', '--inputFile',
						type=str,
						help="The path to the input certificates file.",
						required=True)
	parser.add_argument('-o', '--on_netsFolder',
						type=str,
						help="The path to the on-nets folder.",
						required=True)
	parser.add_argument('-a', '--ipToASFile',
						type=str,
						help="The path of the IP-to-AS file.",
						required=True)

	args = parser.parse_args()

	filePathToStoreResults = "/".join(args.inputFile.split("/")[:-1]) + "/off-nets/"
	createFilePaths(filePathToStoreResults)

	tld_suffixes = load_tld_suffixes()
	ip_to_as = load_ip_to_as_mapping(args.ipToASFile)
	hg_asn_to_hg_keyword, _ = load_hypergiant_ases(args.date)

	dns_names_per_hg = generate_on_net_fingerprints(args.on_netsFolder, tld_suffixes)

	process_off_nets(args.inputFile, ip_to_as, dns_names_per_hg, hg_asn_to_hg_keyword, tld_suffixes, filePathToStoreResults)










