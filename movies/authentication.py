# verify authenticity of telegram login data
import hashlib, collections, hmac
def verify_auth(data, token):
    secret = hashlib.sha256()
    secret.update(token.encode('utf-8'))
    sorted_params = collections.OrderedDict(sorted(data.items()))
    params_hash = sorted_params.pop('hash')
    msg = '\n'.join(['{}={}'.format(k, v) for k, v in sorted_params.items()])

    if params_hash == hmac.new(secret.digest(), msg.encode('utf-8'), hashlib.sha256).hexdigest():
        return True
    return False