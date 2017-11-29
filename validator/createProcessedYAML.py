import os
import ruamel.yaml as yaml
import warnings as warnings

import constants

headersToIgnore = ['next_page', 'current_offset']


def create_processed_yaml(yaml_file):
    """ Create a yaml file that is easy for dredd to process

    :param yaml_file: The original swagger.yaml file to be processed
    """
    yaml_file.pop('externalDocs', None)
    paths = yaml_file.get('paths')
    remove_headers(paths)
    append_x_example(paths)
    file_directory = os.path.dirname(__file__)
    relaxed_swagger = os.path.join(file_directory, constants.SWAGGER)
    with open(relaxed_swagger, 'w') as warning_yaml_file:
        yaml.dump(yaml_file, warning_yaml_file, allow_unicode=True)


def remove_headers(properties):
    """
    Some headers are allowed to not exist when there are not enough tools to be displayed.
    These headers are mentioned in the headersToIgnore global variable above

    :param properties: A dictionary that may contain the headers to ignore
    """
    for single_property in properties.keys():
        if single_property in headersToIgnore:
            for header in headersToIgnore:
                properties.pop(header, None)
        else:
            if isinstance(properties.get(single_property), dict):
                remove_headers(properties.get(single_property))


def append_x_example(paths):
    """
    Dredd depends on x-example to test endpoints with path parameters
    :param paths: Paths described by the swagger yaml
    """
    for path_key in paths:
        path_value = paths.get(path_key)
        parameters = path_value.get('get').get('parameters')
        if parameters is not None:
            for parameter in parameters:
                if parameter.get('in') == 'path':
                    parameter['x-example'] = parameter.get('name') + '_placeholder'


def main():
    """
    The main function to create the processed swagger yaml from an existing preprocessed swagger yaml
    """
    file_directory = os.path.dirname(__file__)
    swagger = os.path.join(file_directory, constants.PREPROCESSED_SWAGGER)
    warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)
    with open(swagger, 'r') as f:
        loaded = yaml.load(f)
        create_processed_yaml(loaded)


if __name__ == '__main__':
    main()

