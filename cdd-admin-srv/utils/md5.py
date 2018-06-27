import hashlib


def encrypt(data, secret_key):
    keys = list(data.keys())
    keys.sort()

    param_list = []
    for key in keys:
        param = '='.join([key, str(data[key])])
        param_list.append(param)
    params_str = '&'.join(param_list)

    source_str = '{params_str}&key={secret_key}'.format(params_str=params_str, secret_key=secret_key)
    print(source_str)

    hl = hashlib.md5()
    hl.update(source_str.encode(encoding='utf-8'))
    target_str = hl.hexdigest()
    print(target_str)

    return target_str.upper()
