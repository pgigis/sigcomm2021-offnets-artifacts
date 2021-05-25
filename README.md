# _"Seven Years in the Life of Hypergiants' Off-Nets"_
## ACM SIGCOMM 2021 Artifacts
Table of Contents
* [Getting Started](#getting-started)
    * [Prerequisites and Installation](#prerequisites-and-installation)
    * [Getting Acccess to the Datasets](#getting-acccess-to-the-datasets

## Getting Started
### Prerequisites and Installation
The entire software was written in python3, which has to be pre-installed on your system.


Install pip3:
```
sudo apt-get install python3-pip
```

In order to isolate the following installation and runs from other parts of the system, we can run everything in a python3 venv environment. This can be done according to the instructions on the
[python3 venv tutorial](https://docs.python.org/3/tutorial/venv.html).

Please follow the aforementioned guide to set up such an environment on your system.

Then, install the required python3 packages within the venv:
```
pip3 install -r requirements.txt
```
In case a required dependency is missing please contact [p.gkigkis at cs.ucl.ac.uk]().

### Getting Acccess to the Datasets
The main dataset that we use for the longitudinal study (e.g., TLS/SSL certificates, HTTP(S) headers), is derived from the [Rapid7 - Open Data](https://opendata.rapid7.com) platform. 

To access the historical dataset you have to apply for an account. 
```Data access is free to Practitioners, Academics, and Researchers.```

To create an account to the Rapid7 Opendata platform visit:
https://opendata.rapid7.com/sonar.ssl/

Then search "Gain Unlimited Access to Our Datasets" and click on "Create a free account".
To fully reproduce our findings, you will need gain access to the following datasets.
* SSL Certificates
* More SSL Certificates (non-443)
* HTTP GET Responses
* HTTPS GET Responses

### TLS certificate data
In this work, we use the following three sources of TLS certificate datasets.
* Rapid7  
* Active Scan (Certigo)
* Censys



## Analysis

### **Step 0**:
```
cd analysis
```

### **Step 1**: Extract End-Entity (EE) certificates.

As first this step, the script takes as an input the certificate dataset and extracts the EE certificate of each IP.
Expired, self-signed and root/intermediate certificates that are not present in the CCADB [Common CA Database](https://www.ccadb.org) are filtered out.

Currently, as an input we support the following two datasets:

1) Active Scan (Certigo)
2) Rapid7 Certificates 

To run the script, execute the following command:
```
python3 extract_valid_certs.py -d 21-11-2019 -t active -i ../datasets/certificates/active/
```

This will generate the folder "active_21-11-2019" inside the "analysis/results" directorty.
Inside the folder it will create a single JSON line-by-line file "ee_certs.txt". Each line contains a JSON object formatted as:
```
{ "ip" : "EndEntity-Certificate" }
```


### **Step 2**: Find TLS fingerprints using hypergiant on-net certificates.
The script takes as an input the generated file of step 1, the configuration file, the list of HG ASes and, the IP-to-AS mapping.

The configuration file contains a mapping between the candidate HG keyword and the HG ASes.
Below is an example of a configuration file. 
```
{"hypergiant-keyword" : "google", "hypergiant-ases-key" : "google"}
{"hypergiant-keyword" : "facebook", "hypergiant-ases-key" : "facebook"}
{"hypergiant-keyword" : "netflix", "hypergiant-ases-key" : "netflix"}
{"hypergiant-keyword" : "akamai", "hypergiant-ases-key" : "akamai"}
{"hypergiant-keyword" : "alibaba", "hypergiant-ases-key" : "alibaba"}
{"hypergiant-keyword" : "youtube", "hypergiant-ases-key" : "google"}
```

Any value can be used as a ```"hypergiant-keyword".``` For the ```"hypergiant-ases-key"``` we support the following values:
```
['yahoo', 'cdnetworks', 'limelight', 'microsoft', 'chinacache', 'apple', 'alibaba', 'amazon', 'akamai', 'bitgravity', 'cachefly', 'cloudflare', 'disney', 'facebook', 'google', 'highwinds', 'hulu', 'incapsula', 'netflix', 'cdn77', 'twitter', 'fastly']
```

To run the script, execute the following command:
```
python3 extract_hypergiant_on-net_certs.py -s ../datasets/hypergiants/2019_11_hypergiants_asns.json  -i results/active_21-11-2019/ee_certs.txt  -c config.json -a ../datasets/ip_to_as/2019_11_25thres_db.json
```

This will create a new folder ```"on-nets"``` inside ```"analysis/results/active\_21-11-2019/"```. The folder contains a file per HG keyword. Each file includes only the ```*dns_names*``` and ```*subject:organization*``` fields of the EE certificates found in IP addresses of the HG AS(es) using this specific keyword. 

Below is an output example. 
```
{"ip": "23.72.3.228", "ASN": 16625, "dns_names": ["try.akamai.com", "threatresearch.akamai.com"], "subject:organization": "akamai technologies, inc. "}
{"ip": "23.223.192.18", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
{"ip": "172.232.1.72", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
{"ip": "210.61.248.97", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
```


### **Step 3**: Find candidate hypergiant off-nets. 
The script takes as an input the generated file of step 1, the generated folder of step 2 that contains the on-net fingerprints, the list of HG ASes and, the IP-to-AS mapping.

To run the script, execute the following command:
```
python3 extract_hypergiant_off-net_certs.py -s ../datasets/hypergiants/2019_11_hypergiants_asns.json -i results/active_21-11-2019/ee_certs.txt -c config.txt -a ../datasets/ip_to_as/2019_11_25thres_db.json -o results/active_21-11-2019/on-nets
```

This will create a new folder ```"candidate\_off-nets"``` inside ```"analysis/results/active\_21-11-2019/"```. The folder contains a file per HG keyword. Each file includes only the ```*dns_names*``` and ```*subject:organization*``` fields of the EE certificates found in IP addresses outside of the HG AS(es) using this specific keyword. 

```
{"ip": "80.239.236.44", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 1299}
{"ip": "2.18.52.28", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 33905}
{"ip": "2.16.173.163", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 20940}
{"ip": "77.94.66.28", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 60772}
```


### **Step 4**: Parse HTTP and HTTPS headers.
**Step 4.1** Pipe the Rapid7 data file to the ```parse_rapid7.py``` script. The command below works well.
```
gunzip -kc 2019-11-18-1574084778-https_get_443.json.gz | ./parse_rapid7.py | awk -F'\t' '{ if(NF == 2) print $0 }' | gzip > 20191118-https.gz
```
That script outputs a tab separated line with ```<ip>\t<header-list>```. Each header name, header value pair is separated by ":", and each header pair is separated by "|".
The script contains a list of "uninteresting" headers which are ignored (e.g. "Server: Apache/PHP"). IP values without "interesting" headers or any headers are output with an empty ```header-list``` so we can keep track of IPs missing from the dataset.

Below is an output example. 
```
104.24.40.135   Set-Cookie:__cfduid=d388387dd3c34cc6c4e37c62d3bc4beb91574121663; expires=Wed, 18-Nov-20 00:01:03 GMT; path=/; domain=.104.24.40.135; HttpOnly|Server:cloudflare|CF-RAY:537de84e0b49ed37-SJC
23.231.139.150
45.38.39.238
167.82.1.144    Server:Varnish|X-Served-By:cache-bur17520-BUR|Via:1.1 varnish
107.165.5.254   Upgrade:h2
104.25.187.85   Set-Cookie:__cfduid=d51c717c0d086ff466c032113ed7265601574121664; expires=Wed, 18-Nov-20 00:01:04 GMT; path=/; domain=.104.25.187.85; HttpOnly|Server:cloudflare|CF-RAY:537de8506816ed2f-SJC
23.57.49.186    Server:AkamaiGHost
```

**Step 4.2** Apply the header rules in hypergiant-headers.txt to the file generated in step 2.
```
gunzip -kc 20191118-http.gz | python3 ./map_networks.py | gzip > 20191118-http-mapped.txt.gz
```

The ```map_networks.py``` script outputs a tab separated line of ```ip, network, asn, asn_name, header_match```. IPs with no CDN header matches are also output to keep track of what IPs are present in the data.

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



**Step 5**: Compare TLS/SSL certificates inferences with HTTP(s) headers.

```
python3 compare_cert_headers.py
```
