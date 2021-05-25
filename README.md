# ACM SIGCOMM 2021 Artifacts
## _"Seven Years in the Life of Hypergiants' Off-Nets"_

Getting Acccess to the Datasets:


The main dataset (e.g. TLS/SSL certificates, HTTP(s) headers) of the paper is provided by Rapid7. 

To access the historical dataset you have to apply for an account. Data access is free to Practitioners, Academics, and Researchers.

To create an account to the Rapid7 Opendata platform visit:
https://opendata.rapid7.com/sonar.ssl/

Then search "Gain Unlimited Access to Our Datasets" and click on "Create a free account".
To fully reproduce our findings, you will need gain access to the following datasets.
* SSL Certificates
* More SSL Certificates (non-443)
* HTTP GET Responses
* HTTPS GET Responses


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


### Analysis

**Step 0**:
```
cd analysis
```

**Step 1**: Extract End-Entity (EE) certificates.

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


**Step 2**: Find TLS fingerprints using hypergiant on-net certificates.
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

Any value can be used as a "hypergiant-keyword". For the "hypergiant-ases-key" we support the following values:
```
['yahoo', 'cdnetworks', 'limelight', 'microsoft', 'chinacache', 'apple', 'alibaba', 'amazon', 'akamai', 'bitgravity', 'cachefly', 'cloudflare', 'disney', 'facebook', 'google', 'highwinds', 'hulu', 'incapsula', 'netflix', 'cdn77', 'twitter', 'fastly']
```

To run the script, execute the following command:
```
python3 extract_hypergiant_on-net_certs.py -s ../datasets/hypergiants/2019_11_hypergiants_asns.json  -i results/active_21-11-2019/ee_certs.txt  -c config.json -a ../datasets/ip_to_as/2019_11_25thres_db.json
```

This will create a new folder "on-nets" inside "analysis/results/active\_21-11-2019/". The folder contains a file per HG keyword. Each file includes only the *dns_names* and *subject:organization* fields of the EE certificates found in IP addresses of the HG AS(es) using this specific keyword. 

Below is an output example. 
```
{"ip": "23.72.3.228", "ASN": 16625, "dns_names": ["try.akamai.com", "threatresearch.akamai.com"], "subject:organization": "akamai technologies, inc. "}
{"ip": "23.223.192.18", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
{"ip": "172.232.1.72", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
{"ip": "210.61.248.97", "ASN": 20940, "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. "}
```


**Step 3**: Find candidate hypergiant off-nets. 
The script takes as an input the generated file of step 1, the generated folder of step 2 that contains the on-net fingerprints, the list of HG ASes and, the IP-to-AS mapping.

To run the script, execute the following command:
```
python3 extract_hypergiant_off-net_certs.py -s ../datasets/hypergiants/2019_11_hypergiants_asns.json -i results/active_21-11-2019/ee_certs.txt -c config.txt -a ../datasets/ip_to_as/2019_11_25thres_db.json -o results/active_21-11-2019/on-nets
```

This will create a new folder "candidate\_off-nets" inside "analysis/results/active\_21-11-2019/". The folder contains a file per HG keyword. Each file includes only the *dns_names* and *subject:organization* fields of the EE certificates found in IP addresses outside of the HG AS(es) using this specific keyword. 

```
{"ip": "80.239.236.44", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 1299}
{"ip": "2.18.52.28", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 33905}
{"ip": "2.16.173.163", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 20940}
{"ip": "77.94.66.28", "dns_names": ["a248.e.akamai.net", "*.akamaized-staging.net", "*.akamaized.net", "*.akamaihd-staging.net", "*.akamaihd.net"], "subject:organization": "akamai technologies, inc. ", "ASN": 60772}
```


**Step 4**: Parse HTTP and HTTPS headers.





**Step 5**: Compare TLS/SSL certificates inferences with HTTP(s) headers.

```
python3 compare_cert_headers.py
```