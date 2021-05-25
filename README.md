# _"Seven Years in the Life of Hypergiants' Off-Nets"_
## ACM SIGCOMM 2021 Artifacts
Table of Contents
* [Getting Started](#getting-started)
    * [Prerequisites and Installation](#prerequisites-and-installation)
    * [Getting Acccess to the Datasets](#getting-acccess-to-the-datasets)
* [Analysis](#analysis)


## Getting Started
### Prerequisites and Installation
The entire software was written in python3, which has to be pre-installed on your system.

Install pip3:
```
sudo apt-get install python3-pip
```

In order to isolate the following installation and runs from other parts of the system, we can run everything in a python3 venv environment. This can be done according to the instructions on the
[python3 venv tutorial](https://docs.python.org/3/tutorial/venv.html).

Please, follow the aforementioned guide to set up an environment on your system.

Then, install the required python3 packages within the venv:
```
pip3 install -r requirements.txt
```
In case a required dependency is missing, please contact [p.gkigkis at cs.ucl.ac.uk]().


### Getting Acccess to the Datasets
Our methodology uses TLS certificate scans as a building block, supplementing them with additional techniques (e.g., HTTP(S) fingerprints) and datasets (e.g., APNIC population estimates, CAIDA AS Relationship Dataset, IP-to-AS mapping, etc..). 

We document in detail the datasets [here]().

In addition to this GitHub repository, we provide an OneDrive directory which contains additional datasets used in this work.

For our longitudinal analysis, we used TLS certificate scans and HTTP(S) headers, derived from the [Rapid7 - Open Data](https://opendata.rapid7.com) platform.

To access the historical datasets of Rapid7 Open Data platform you need to apply for an account.
```Data access is free to Practitioners, Academics, and Researchers.```

To create an account to the Rapid7 Opendata platform visit:
https://opendata.rapid7.com/sonar.ssl/

Then search "Gain Unlimited Access to Our Datasets" (located close to the bottom of the page) and click on "Create a free account".
To fully reproduce our findings, you will need to gain access to the following datasets.
* SSL Certificates
* More SSL Certificates (non-443)
* HTTP GET Responses
* HTTPS GET Responses

We provide a detailed documentation, on how to download and process the Rapid7 dataset here.

Except the Rapid7 certificates we also used TLS certificate data derived from an active scan that we conducted in Nov. 2019
but also data derived from the [Censys](https://censys.io/) platflorm. You can read more on how to obtain Research access to the Censys platform [here](https://support.censys.io/hc/en-us/articles/360038761891-Research-Access-to-Censys-Data).


## Analysis
For the analysis part, we suggest to populate the ```datasets``` folder of this repository, following these [instructions](https://github.com/pgigis/sigcomm2021-offnets-artifacts/tree/readme/datasets).
The next steps suffice to infer the off-nets of the considered Hypergiants in this study. We will include more analysis commands that are available in the software at a later stage.


### **Step 0**:
```
cd analysis
```

### **Step 1**: Extract End-Entity (EE) certificates.

As a first step, the script takes as an input the certificate dataset and extracts the End-Entity (EE) certificate of each IP.
Expired, self-signed and root/intermediate certificates that are not present in the CCADB [Common CA Database](https://www.ccadb.org) are filtered out.

Currently, as an input we support the following two datasets:

1) Active Scan (Certigo) - *Suggested*
2) Rapid7 TLS scans 

To run the script, execute the following command:
```
python3 extract_valid_certs.py -d 21-11-2019 -t active -i ../datasets/certificates/active/
```

This will generate the folder "active_21-11-2019" inside the "analysis/results".
Inside the folder it will create a single JSON line-by-line file "ee_certs.txt". Each line contains a JSON object formatted as:
```
{ "ip" : "EndEntity-Certificate" }
```


### **Step 2**: Find TLS fingerprints using hypergiant on-net certificates.
Script ```extract_hypergiant_on-net_certs.py``` takes as an input the generated file of step 1, the configuration file, the list of HG ASes and, the IP-to-AS mapping.

The configuration file contains a mapping between the candidate HG keyword and the HG ASes.
Here is an example of a configuration file. 
```
{"hypergiant-keyword" : "google", "hypergiant-ases-key" : "google"}
{"hypergiant-keyword" : "facebook", "hypergiant-ases-key" : "facebook"}
{"hypergiant-keyword" : "netflix", "hypergiant-ases-key" : "netflix"}
{"hypergiant-keyword" : "akamai", "hypergiant-ases-key" : "akamai"}
{"hypergiant-keyword" : "alibaba", "hypergiant-ases-key" : "alibaba"}
```

Any value can be used as a ```"hypergiant-keyword"```. For the ```"hypergiant-ases-key"``` we support the following values:
```
['yahoo', 'cdnetworks', 'limelight', 'microsoft', 'chinacache', 'apple', 'alibaba', 'amazon', 'akamai', 'bitgravity', 'cachefly', 'cloudflare', 'disney', 'facebook', 'google', 'highwinds', 'hulu', 'incapsula', 'netflix', 'cdn77', 'twitter', 'fastly']
```

To run the script, execute the following command:
```
python3 extract_hypergiant_on-net_certs.py -s ../datasets/hypergiants/2019_11_hypergiants_asns.json  -i results/active_21-11-2019/ee_certs.txt  -c config.json -a ../datasets/ip_to_as/2019_11_25thres_db.json
```

This will create a folder ```"on-nets"``` inside ```"analysis/results/active_21-11-2019/"```. The folder contains a file per HG keyword. Each file includes only the ```dns_names``` and ```subject:organization``` fields of the EE certificates found in IP addresses of the HG AS(es) using this specific keyword. 

Here is an output example. 
```
{"ip": "23.72.3.228", "ASN": 16625, "dns_names": ["try.akamai.com", "threatresearch.akamai.com"], "subject:organization": "akamai technologies, inc. "}
{"ip": "23.223.192.18", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
{"ip": "172.232.1.72", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
{"ip": "210.61.248.97", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
```


### **Step 3**: Find candidate hypergiant off-nets. 
Script ```extract_hypergiant_off-net_certs.py``` takes as an input the generated file of step 1, the generated folder of step 2, the list of HG ASes and, the IP-to-AS mapping.

To run the script, execute the following command:
```
python3 extract_hypergiant_off-net_certs.py -s ../datasets/hypergiants/2019_11_hypergiants_asns.json -i results/active_21-11-2019/ee_certs.txt -c config.txt -a ../datasets/ip_to_as/2019_11_25thres_db.json -o results/active_21-11-2019/on-nets
```

This will create a folder ```"candidate_off-nets"``` inside ```"analysis/results/active_21-11-2019/"```. The folder contains a file per HG keyword. Each file includes only the ```dns_names``` and ```subject:organization``` fields of the EE certificates found in IP addresses outside of the HG AS(es) using this specific keyword. 

Here is an output example. 
```
{"ip": "80.239.236.44", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 1299}
{"ip": "2.18.52.28", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 33905}
{"ip": "2.16.173.163", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 20940}
{"ip": "77.94.66.28", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 60772}
```


### **Step 4**: Parse HTTP and HTTPS headers.
Please, refer here on how to obtain the HTTP(S) header files. Due to the size of these files (~60GB compressed), we suggest to not completely uncompress them.
In our analysis, we always use the ```gunzip -kc``` flags to keep the files compressed, while sending the output to stdout.

**Step 4.1** Find the HTTP(S) header names.

Execute the following command:
```
gunzip -kc 2019-11-18-1574084778-https_get_443.json.gz | ./parse_rapid7.py | awk -F'\t' '{ if(NF == 2) print $0 }' | gzip > 20191118-https.gz
```

The output of the script is a tab separated line with ```<ip>\t<header-list>```. Each header name and header value pair is separated by ":", and each header pair is separated by "|". The script contains a list of "uninteresting" headers which are ignored (e.g., "Server: Apache/PHP"). Finally, IP values without "interesting" headers or any headers at all, are output with an empty ```header-list```, so we can keep track of IP addresses missing from the dataset.

Here is an output example. 
```
104.24.40.135   Set-Cookie:__cfduid=d388387dd3c34cc6c4e37c62d3bc4beb91574121663; expires=Wed, 18-Nov-20 00:01:03 GMT; path=/; domain=.104.24.40.135; HttpOnly|Server:cloudflare|CF-RAY:537de84e0b49ed37-SJC
23.231.139.150
45.38.39.238
167.82.1.144    Server:Varnish|X-Served-By:cache-bur17520-BUR|Via:1.1 varnish
107.165.5.254   Upgrade:h2
104.25.187.85   Set-Cookie:__cfduid=d51c717c0d086ff466c032113ed7265601574121664; expires=Wed, 18-Nov-20 00:01:04 GMT; path=/; domain=.104.25.187.85; HttpOnly|Server:cloudflare|CF-RAY:537de8506816ed2f-SJC
23.57.49.186    Server:AkamaiGHost
```

**Step 4.2** Apply the header rules in hypergiant-headers.txt to the file generated in step 4.1.

The ```map_networks.py``` script outputs a tab separated line of ```ip, network, asn_name, header_match```. IPs with no CDN header matches are also output to keep track of what IPs exist in the data.

Execute the following command:
```
gunzip -kc 20191118-http.gz | python3 ./map_networks.py | gzip > 20191118-http-mapped.txt.gz
```

Here is an output example. 
```
104.24.40.135   Cloudflare      13335   CLOUDFLARENET; US       server:cloudflare
23.231.139.150
45.38.39.238
167.82.1.144    Fastly  54113   FASTLY; US      x-served-by:cache-bur17520-bur
104.25.187.85   Cloudflare      13335   CLOUDFLARENET; US       server:cloudflare
23.57.49.186    Akamai  16625   AKAMAI-AS; US   server:akamaighost
104.18.84.77    Cloudflare      13335   CLOUDFLARENET; US       server:cloudflare
216.172.167.24
104.144.176.112 Alibaba 55286   SERVER-MANIA; CA        server:tengine/2.0.0
```

### **Step 5**: Compare TLS/SSL certificates inferences with HTTP(s) headers.

Execute the following command:
```
python3 compare_cert_headers.py
```



