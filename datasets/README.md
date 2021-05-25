# Datasets

Due to the size of the datasets, we provide [here](https://liveuclac-my.sharepoint.com/:f:/g/personal/ucabpgk_ucl_ac_uk/Eim32GoBUgVOoLolQCYbbyMBSf-PiNBbOzuQl52n3Xm94w?e=7GOz5l) an OneDrive directory, that contains additional datasets used in this work.

For our longitudinal analysis, we used TLS certificate scans and HTTP(S) headers, derived from the [Rapid7 - Open Data](https://opendata.rapid7.com) platform.

## Rapid7 Datasets

### Download data

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

We provide a detailed documentation, on how to download and process the Rapid7 dataset [here](https://github.com/pgigis/sigcomm2021-offnets-artifacts/tree/readme/datasets).

Except the Rapid7 certificates we also used TLS certificate data derived from an active scan that we conducted in Nov. 2019
but also from the [Censys](https://censys.io/) platflorm. You can read more on how to obtain Research access to the Censys platform [here](https://support.censys.io/hc/en-us/articles/360038761891-Research-Access-to-Censys-Data).

## How to download a file from Rapid7 Open Data platform
At first you need to an acount and create an API key.

After this, using the following command you can request a download link from Rapid7. (Note: The link is only valid for a few hours.)
```
curl -H "X-Api-Key: XXX" https://us.api.insight.rapid7.com/opendata/studies/<DATASET-NAME>/<FILENAME>/download/
```
To successfully execute the above command, you will need an API key, the dataset name (e.g., sonar.http or sonar.https) and the download file name (e.g., 2019-11-18-1574121404-http_get_80.json.gz).

Then, you will received a download link and using the example below, you can resume the download if it interrupted and will work even if you use a new URL.
```
curl -L -o 2019-11-18-1574121404-http_get_80.json.gz -C - https://f002.backblazeb2.com/file/rapid7-opendata/sonar.http/2019-11-18-1574121404-http_get_80.json.gz?Authorization=30023402023
```

The official Rapid7 Open Data API help is [here](https://opendata.rapid7.com/apihelp/).


### TLS/SSL scans

The TLS/SSL scans that we used in our longitudinal analysis can be found [here](https://opendata.rapid7.com/sonar.ssl/). In our study we used HTTPS GET requests on port-443. More specifically, in our analysis we use the ```_hosts``` and ```_certs``` files.

According to the Rapid7 dataset [documentation](https://opendata.rapid7.com/sonar.ssl/): 

> The ```_hosts``` files provide mapping between the IPs/endpoints and the fingerprint of the X.509 certificate presented.
> The ```_certs``` file provides a mapping of the net new certificates from a given study and the corresponding fingerprint. 

In our analysis we had to download all ```_certs``` available to construct a global mapping between fingerprints and the raw certificate in PEM format.
Moreover, we found that some fingerprints where not present in the related to HTTPS GET port-443 files and we downloaded all ```_certs``` of both available TLS/SSL certificate datasets ([SSL Certificates](https://opendata.rapid7.com/sonar.ssl/) and [More SSL Certificates (non-443)](https://opendata.rapid7.com/sonar.moressl/)). We list exactly which files we used to construct the fingerprint to certificate in PEM format [here-1](https://github.com/pgigis/sigcomm2021-offnets-artifacts/blob/master/datasets/tls_scans/rapid7/certificates/ssl_certificates_https_443_filenames.txt), [here-2](https://github.com/pgigis/sigcomm2021-offnets-artifacts/blob/master/datasets/tls_scans/rapid7/certificates/more_ssl_certificates_non_443_filenames.txt) and [here-3](https://github.com/pgigis/sigcomm2021-offnets-artifacts/blob/master/datasets/tls_scans/rapid7/certificates/ssl_certificates_https_non_443_filenames.txt). 

### HTTP headers
The HTTP GET Responses that we used in our analysis can be found [here](https://github.com/pgigis/sigcomm2021-offnets-artifacts/blob/master/datasets/headers/http/http_80_filenames.txt).

### HTTPS headers
The HTTPS GET Responses that we used in our analysis can be found [here](https://github.com/pgigis/sigcomm2021-offnets-artifacts/blob/master/datasets/headers/https/https_443_filenames.txt).

## Active Scan

As we use a snapshot every three months (January, April, July, October), we alligned each dataset to the closest available date.

## IP-to-AS Mapping

The IP-to-AS mappings that we used in this work can be [here](https://liveuclac-my.sharepoint.com/:f:/g/personal/ucabpgk_ucl_ac_uk/EujvVAp0lqBBpY-EgY5IZSgBLTgoxv7xwtRW92YGe9hDLA?e=2iSwLV).

Please copy the contents of the OneDrive folder in the ```ip_to_as``` folder.


