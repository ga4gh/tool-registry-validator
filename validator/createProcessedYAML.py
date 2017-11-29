import os
import ruamel.yaml as yaml
import warnings as warnings

import constants

headersToIgnore = ['next_page', 'current_offset']


# Creating another YAML that is less strict than the original
def create_processed_yaml(yaml_file):
    yaml_file.pop('externalDocs', None)
    paths = yaml_file.get('paths')
    remove_headers(paths)
    append_x_example(paths)
    file_directory = os.path.dirname(__file__)
    relaxed_swagger = os.path.join(file_directory, constants.SWAGGER)
    with open(relaxed_swagger, 'w') as warning_yaml_file:
        yaml.dump(yaml_file, warning_yaml_file, allow_unicode=True)


# Some headers are allowed to not exist when there are not enough tools to be displayed
def remove_headers(properties):
    for single_property in properties.keys():
        if single_property in headersToIgnore:
            for header in headersToIgnore:
                properties.pop(header, None)
        else:
            if isinstance(properties.get(single_property), dict):
                remove_headers(properties.get(single_property))


def append_x_example(paths):
    for path_key in paths:
        path_value = paths.get(path_key)
        parameters = path_value.get('get').get('parameters')
        if parameters is not None:
            for parameter in parameters:
                if parameter.get('in') == 'path':
                    parameter['x-example'] = parameter.get('name') + '_placeholder'


if __name__ == '__main__':
    fileDirectory = os.path.dirname(__file__)
    swagger = os.path.join(fileDirectory, constants.PREPROCESSED_SWAGGER)
    warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)
    with open(swagger, 'r') as f:
        loaded = yaml.load(f)
        create_processed_yaml(loaded)
