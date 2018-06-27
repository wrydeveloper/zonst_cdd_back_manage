import hashlib


def hexdigest_password(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = raw_password, salt
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not \
                supported in this environment')
        return crypt.crypt(raw_password, salt)

    salt_password_str = '%s%s' % (salt, raw_password)

    if algorithm == 'md5':
        return hashlib.md5(salt_password_str.encode('utf-8')).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt_password_str.encode('utf-8')).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def sort_hash_urlencode(d, pop_keys=None):
    """对字典进行排序, 按照key的顺序从小到大进行排列"""
    d2 = d.copy()

    # 剔除不参与排序的key
    if pop_keys is not None:
        for k in pop_keys:
            if k in d2:
                d2.pop(k)

    d3 = sorted(d2.items(), key=lambda m: m[0])
    return "&".join(['%s=%s' % i for i in d3])


def hexdigest_hash(pop_keys=None, **kwargs):
    """对请求参数进行签名"""
    if 'secret_key' not in kwargs:
        raise Exception("secret_key is required.")
    secert_key = kwargs.pop('secret_key')

    request_str = sort_hash_urlencode(kwargs, pop_keys=pop_keys)
    unsigned_str = "%s%s" % (request_str, secert_key)
    return hashlib.md5(unsigned_str.encode('utf-8')).hexdigest()
