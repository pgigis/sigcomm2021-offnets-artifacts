# ACM SIGCOMM 2021 Artifacts
## _"Seven Years in the Life of Hypergiants' Off-Nets"_

Getting Acccess to the Datasets:

The main dataset (e.g. TLS/SSL certificates, HTTP(s) headers) of the paper is provided by Rapid7. 

To access the historical dataset you have to apply in rapid7 for an account. Data access is free to Practitioners, Academics, and Researchers.

To create an account to the Rapid7 Opendata platform visit:
https://opendata.rapid7.com/sonar.ssl/

Then search "Gain Unlimited Access to Our Datasets" and click on "Create a free account".
To fully reproduce our findings, you will need gain access to the following datasets.
* SSL Certificates
* More SSL Certificates (non-443)
* HTTP GET Responses
* HTTPS GET Responses



### Analysis

**Step 1**: Extract valid certificates.

In this step, the script takes as an input the certificate dataset and excludes expired, self-signed and ce non-trusted chain.

The script supports the following input datasets.

Two inputs:

1) Active Scan
2) Rapid7 Certificates

This will generate, a single JSON line-by-line file. Each line contains a JSON object
with the following format:

```
{ "ip" : "EndEntity-Certificate" }
```

**Step 2**: Extract hypergiant.

The script takes as an input the generated file from step 1 and the hypergiant keyword (e.g., google).

This will generate, a file with all hypergiant certificates founds in on-net IP addresses.


**Step 3**:
Search in the off-nets for IPs with certificates of the HG

Takes as an input the Hypergiant keyword


**Step 4**: Process HTTP and HTTPs.


**Step 5**: Compare TLS/SSL certificates inferences with HTTP(s) headers.


