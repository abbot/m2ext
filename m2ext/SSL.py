from M2Crypto import SSL, X509
import _m2ext

class Context(SSL.Context):
    def validate_certificate(self, cert):
        """
        Validate a certificate using this SSL Context
        """
        store_ctx = X509.X509_Store_Context(_m2ext.x509_store_ctx_new(), _pyfree=1)
        _m2ext.x509_store_ctx_init(store_ctx.ctx,
                                   self.get_cert_store().store,
                                   cert.x509, None)
        rc = _m2ext.x509_verify_cert(store_ctx.ctx)
        if rc < 0:
            raise SSL.SSLError("Empty context")
        return rc != 0
