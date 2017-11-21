import dredd_hooks as hooks

response_stash = {}
id = "registry.hub.docker.com%2Fsequenza%2Fsequenza"
api_uri = "XXX"
DEFAULT_TYPE = 'CWL'
DEFAULT_RELATIVE_PATH = '/sequenza.cwl'
DEFAULT_VERSION_ID = 'latest'
DEFAULT_ID = 'registry.hub.docker.com/sequenza/sequenza'


@hooks.before_each
def add_token(transaction):
    transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_ID,
                                                              'registry.hub.docker.com%2Fsequenza%2Fsequenza')
    transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_VERSION_ID, 'latest')
    transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_TYPE, 'CWL')
    transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_RELATIVE_PATH, '%2Fsequenza.cwl')


@hooks.before_each_validation
def relax_headers(transaction):
    try:
        real_content_type = transaction['real']['headers']['content-type']
        expected_content_type = transaction['expected']['headers']['Content-Type']
        if expected_content_type in real_content_type:
            transaction['expected']['headers']['Content-Type'] = real_content_type
    except KeyError:
        return
