%module _m2ext

%{
#include <openssl/err.h>
#include <openssl/rand.h>
%}

%include <openssl/opensslv.h>

%{
#include <openssl/x509.h>
#include <openssl/ssl.h>
#include <openssl/x509v3.h>
#include <openssl/stack.h>

#if OPENSSL_VERSION_NUMBER >= 0x10000000L
#define STACK _STACK
#endif
%}

%rename(x509_store_ctx_new) X509_STORE_CTX_new;
extern X509_STORE_CTX *X509_STORE_CTX_new(void);


%inline %{
int x509_store_ctx_init(X509_STORE_CTX *ctx, X509_STORE *store,
                        X509 *x509, STACK *chain)
{
    return X509_STORE_CTX_init(ctx, store, x509, (STACK_OF(X509)*)chain);
}
%}

%rename(x509_store_ctx_set_purpose) X509_STORE_CTX_set_purpose;
extern int X509_STORE_CTX_set_purpose(X509_STORE_CTX *ctx, int purpose);

%rename(x509_verify_cert) X509_verify_cert;
extern int X509_verify_cert(X509_STORE_CTX *ctx);

%rename(x509_extension_get_object) X509_EXTENSION_get_object;
extern ASN1_OBJECT *	X509_EXTENSION_get_object(X509_EXTENSION *ex);

%inline %{
PyObject *x509_extension_get_data(X509_EXTENSION *ex)
{
    ASN1_OCTET_STRING *data = X509_EXTENSION_get_data(ex);
    return PyString_FromStringAndSize(data->data, data->length);
}
%}

%inline %{
long ssl_ctx_add_extra_chain_cert(SSL_CTX* ctx, X509* x509)
{
    return SSL_CTX_add_extra_chain_cert(ctx, x509);
}
%}
