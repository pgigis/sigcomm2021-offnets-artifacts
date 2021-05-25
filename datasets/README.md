## Download Rapid7 data

The official Rapid7 Open Data API help is [here](https://opendata.rapid7.com/apihelp/).

### TLS/SSL scans

The TLS/SSL scans that we used in our longitudinal analysis can be found [here](https://opendata.rapid7.com/sonar.ssl/). In our study we used HTTPS GET requests on port-443. More specifically, in our analysis we use the ```_hosts``` and ```_certs``` files.

According to the Rapid7 dataset [documentation](https://opendata.rapid7.com/sonar.ssl/): 

> The ```_hosts``` files provide mapping between the IPs/endpoints and the fingerprint of the X.509 certificate presented.
> The ```_certs``` file provides a mapping of the net new certificates from a given study and the corresponding fingerprint. 

In our analysis we had to download all ```_certs``` available to construct a global mapping between fingerprints and the raw certificate in PEM format.
Moreover, we found that some fingerprints where not present in the related to HTTPS GET port-443 files and we downloaded all ```_certs``` of both available TLS/SSL certificate datasets ([SSL Certificates](https://opendata.rapid7.com/sonar.ssl/) and [More SSL Certificates (non-443)](https://opendata.rapid7.com/sonar.moressl/)). We list exactly which files we used to construct the fingerprint to certificate in PEM format [here-1](https://github.com/pgigis/sigcomm2021-offnets-artifacts/blob/master/datasets/tls_scans/rapid7/certificates/ssl_certificates_https_443_filenames.txt), [here-2](https://github.com/pgigis/sigcomm2021-offnets-artifacts/blob/master/datasets/tls_scans/rapid7/certificates/more_ssl_certificates_non_443_filenames.txt) and [here-3](https://github.com/pgigis/sigcomm2021-offnets-artifacts/blob/master/datasets/tls_scans/rapid7/certificates/ssl_certificates_https_non_443_filenames.txt). 

Rapid7 

To run our analysis for a given you need to obtai

a snapshot 

According to Rapid7 

The dataset contains a collection of metadata related to the net new X.509 certificates observed in each study when considering all SSL studies that ran prior. The _hosts and _endpoints files provide mapping between the IPs/endpoints and the fingerprint of the X.509 certificate presented. The _certs file provides a mapping of the net new certificates from a given study and the corresponding fingerprint. The _names file provides a mapping of the X.509 certificate name (CN) to its fingerprint.

### HTTP headers

### HTTPs headers


Available data is browsable from Rapid7
