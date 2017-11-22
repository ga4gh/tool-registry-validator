import os
import ruamel.yaml as yaml
import warnings as warnings

import constants


# Creating another YAML that is less strict than the original
def create_processed_yaml(yaml_file):
    paths = yaml_file.get('paths')
    append_x_example(paths)
    file_directory = os.path.dirname(__file__)
    relaxed_swagger = os.path.join(file_directory, constants.SWAGGER)
    with open(relaxed_swagger, 'w') as warning_yaml_file:
        yaml.dump(yaml_file, warning_yaml_file, allow_unicode=True)


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
