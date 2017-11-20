import dredd_hooks as hooks

response_stash = {}
id = "registry.hub.docker.com%2Fsequenza%2Fsequenza"
api_uri = "XXX"
DEFAULT_TYPE = 'CWL'
DEFAULT_RELATIVE_PATH = '/sequenza.cwl'
DEFAULT_VERSIONID = 'latest'
DEFAULT_ID = 'registry.hub.docker.com/sequenza/sequenza'


@hooks.before_each
def add_token(transaction):
    print transaction
    transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_ID,
                                                              'registry.hub.docker.com%2Fsequenza%2Fsequenza')
    transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_VERSIONID, 'latest')
    transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_TYPE, 'CWL')
    transaction['fullPath'] = transaction['fullPath'].replace(DEFAULT_RELATIVE_PATH, '%2Fsequenza.cwl')
