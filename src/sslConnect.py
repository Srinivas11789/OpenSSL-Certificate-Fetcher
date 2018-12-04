# Module import
from datetime import datetime
import ssl, socket, sys
from OpenSSL import SSL,crypto


class ssl_connect:

    def __init__(self, host, ssl_version=ssl.PROTOCOL_TLSv1):
        self.host = host
        self.ssl_version = ssl_version

    def default_certificate_fetch(self):
        cert = ''

        try:
            cert = ssl.get_server_certificate((self.host, 443), self.ssl_version)
        except Exception as e:
            print ("Could not connect error !! Error is %s") % (e)

        certificate = {}

        if (cert):
            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            certificate.update({"host":self.host})
            certificate.update({"version":x509.get_version()})
            certificate.update({"issuer":x509.get_issuer().get_components()})
            certificate.update({"signature_algorithm":x509.get_signature_algorithm()})
            certificate.update({"parameters": x509.get_subject().get_components()})
            certificate.update({"key_length":x509.get_pubkey().bits()})
            time = x509.get_notBefore()
            certificate.update({"validity_start":time[:8]+time[8:]})
            time = x509.get_notAfter()
            certificate.update({"validity_end":time[:8]+time[8:]})

        return certificate

    def crypto_supported(self):
        # Key exchange cryptography - cipher list
        # ssl.wrap_socket(s, ssl_version=ver, ciphers="ADH-AES256-SHA")
        pass

    def ssl_support(self):
        # Possible Depreceiation Attack
        # ssl.PROTOCOL_SSLv2, ssl.PROTOCOL_SSLv3????

        # TLS versions 1 --> 1.2
        ssl_tls_versions = [ssl.PROTOCOL_TLSv1, ssl.PROTOCOL_TLSv1_1, ssl.PROTOCOL_TLSv1_2]
        data = "Hello SSL"
        port = 443
        result = []
        for ver in ssl_tls_versions:
            # TCP socket creation
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            sslSock = ssl.wrap_socket(s, ssl_version=ver)
            try:
                sslSock.connect((self.host, port))
                sslSock.send(data)
                result.append(True)
                sslSock.close()
            except:
                result.append(False)

        # TLS version 1.3 
        # * there is no constant to enable this in ssl library - Trick: use sslv23 and disable other ssl tls versions
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.protocol = ssl.PROTOCOL_SSLv23
        context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        sslSock = context.wrap_socket(s, server_hostname=self.host)
        try:
            sslSock.connect((self.host, port))
            sslSock.send(data)
            result.append(True)
            sslSock.close()
        except:
            result.append(False)
        return result 
           
def main():
    sslconnection = ssl_connect("google.co.in")
    print sslconnection.default_certificate_fetch()
    sslconnection = ssl_connect("tls13.crypto.mozilla.org")
    print sslconnection.default_certificate_fetch()
    print sslconnection.ssl_support()
    
main()
