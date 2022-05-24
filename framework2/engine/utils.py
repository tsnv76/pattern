@staticmethod
def _get_query_params(environ: dict):
    result = environ['QUERY_STRING']
    query_param = {}
    if result:
        data = result.split('&')
        for item in data:
            k, v = item.split('=')
            if query_param.get(k):
                query_param[k].append(v)
            else:
                query_param[k] = [v]
    return query_param
