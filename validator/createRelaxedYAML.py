import os
import ruamel.yaml as yaml
import warnings as warnings

import constants

toReplace = ['string', 'boolean']
headersToIgnore = ['next_page', 'current_offset']


# Creating another YAML that is less strict than the original
def create_relaxed_yaml(yaml_file):
    definitions = yaml_file.get('definitions')
    replace_with_nullable_types(definitions)
    remove_headers(yaml_file.get('paths'))
    file_directory = os.path.dirname(__file__)
    relaxed_swagger = os.path.join(file_directory, constants.RELAXED_SWAGGER)
    with open(relaxed_swagger, 'w') as warning_yaml_file:
        yaml.dump(yaml_file, warning_yaml_file, allow_unicode=True)


# Some properties are allowed to be null
def replace_with_nullable_types(properties):
    for single_property in properties:
        if single_property == 'type' and properties[single_property] in toReplace:
            properties[single_property] = [properties[single_property], 'null']
        else:
            if isinstance(properties.get(single_property), dict):
                replace_with_nullable_types(properties.get(single_property))


# Some headers are allowed to not exist when there are not enough tools to be displayed
def remove_headers(properties):
    for single_property in properties.keys():
        if single_property in headersToIgnore:
            for header in headersToIgnore:
                properties.pop(header, None)
        else:
            if isinstance(properties.get(single_property), dict):
                remove_headers(properties.get(single_property))


if __name__ == '__main__':
    fileDirectory = os.path.dirname(__file__)
    swagger = os.path.join(fileDirectory, constants.SWAGGER)
    warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)
    with open(swagger, 'r') as f:
        loaded = yaml.load(f)
        create_relaxed_yaml(loaded)
