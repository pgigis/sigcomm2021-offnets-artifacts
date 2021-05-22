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

In this step, the script takes as an input the certificate dataset and extracts the EE certificates.
The script excludes expired, self-signed and root/intermediate certificates that are not present in the CCADB [Common CA Database](https://www.ccadb.org).

Currently, the following two input datasets are supported:

1) Active Scan
2) Rapid7 Certificates

```
python3 extract_ee_certs.py

```

This will generate, a single JSON line-by-line file. Each line contains a JSON object with the following format:

```
{ "ip" : "EndEntity-Certificate" }
```

**Step 2**: Process hypergiant on-net certificates.

The script takes as an input the generated file from step 1 and the hypergiant keyword (e.g., google).
```
python3 extract_hypergiant_on-net_certs.py
```

This will generate, a single JSON line-by-line file that includes only the *dns_names* and *subject:organization* fields of the EE certificates found in IP addresses of the HG AS(es). Each line contains a JSON object with the following format:


```
{ "ip" : { "ASN" : IntegerValue, "dns_names" : [ StringValue, ], "subject:organization" : StringValue } }
```


**Step 3**: Find hypergiant certificates in off-nets. 

Takes as an input the Hypergiant keyword
```
python3 extract_hypergiant_off-net_certs.py
```

This will generate, a single JSON line-by-line file that includes only the *dns_names* and *subject:organization* fields of the EE certificates found in IP addresses of the HG AS(es). Each line contains a JSON object with the following format:


```
{ "ip" : { "ASN" : IntegerValue, "dns_names" : [ StringValue, ], "subject:organization" : StringValue } }
```


**Step 4**: Process HTTP and HTTPs.



**Step 5**: Compare TLS/SSL certificates inferences with HTTP(s) headers.

```
python3 compare_cert_headers.py
```