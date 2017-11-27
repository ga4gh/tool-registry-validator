import ruamel.yaml as yaml
import warnings as warnings
import os
import sys

import constants

global_issues = []


def compare_definitions(yaml1, yaml2):
    definitions1 = yaml1.get('definitions')
    definitions2 = yaml2.get('definitions')
    rename_title_to_definition(definitions2)
    for definition in definitions1:
        # with open(definition, 'w') as yaml_file:
        #     yaml.dump(definitions1.get(definition), yaml_file, allow_unicode=True)
        if definition in definitions2:
            print 'Comparing ' + definition
            definition1 = definitions1.get(definition)
            definition2 = definitions2.get(definition)
            compare_definition(definition1, definition2, definition2, definition2)
        else:
            # Ignore missing Error definition because it definitely is not in proto
            if definition != 'Error':
                print 'Missing definition: ' + definition


def rename_title_to_definition(definitions2):
    for definition in definitions2.keys():
        if definition == 'title':
            definitions2['description'] = definitions2.pop('title')
        else:
            if isinstance(definitions2.get(definition), dict):
                rename_title_to_definition(definitions2.get(definition))


def compare_definition(definition1, definition2, real_definition1, real_definition2):
    added, removed, modified, same = dict_compare(definition2, definition1)
    global global_issues
    if removed:
        # Ignore required properties, protobuf doesn't support it
        removed.discard('required')
        removed.discard('description')
        if removed:
            for removed_property in removed:
                if removed_property == 'type' or removed_property == 'enum':
                    enum_property = definition1.get('enum')
                    type_property = definition1.get('type')
                    ref_property = definition2.get('$ref')
                    # Ignoring this case because conversion to proto messes up the enums
                    if enum_property == ['CWL', 'WDL'] and type_property == 'string' and ref_property is not None:
                        proto_definition = definition2.get('$ref').replace('#/definitions/', '')
                        if proto_definition is not None:
                            print 'Ignoring enum'
                        else:
                            handle_error(removed_property, 'Missing')
                    else:
                        handle_error(removed_property, 'Missing')
                else:
                    handle_error(removed_property, 'Missing')
    if modified:
        for modified_property in modified:
            new = modified.get(modified_property)[0]
            old = modified.get(modified_property)[1]
            if isinstance(new, dict) and isinstance(old, dict):
                compare_definition(old, new, real_definition1, real_definition2)
            else:
                handle_error(modified_property, 'Modified')


def handle_error(problem_property, problem):
    message = problem + ' property: ' + problem_property
    print >> sys.stderr, message
    global global_issues
    global_issues.append(message)


def compare_paths(yaml1, yaml2):
    paths1 = yaml1.get('paths')
    paths2 = yaml2.get('paths')

    base_path = yaml1.get('basePath')
    for path in paths1:
        full_path = base_path + path
        if full_path not in paths2:
            print >> sys.stderr, 'Missing endpoint: ' + path


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same


if __name__ == '__main__':
    fileDirectory = os.path.dirname(__file__)
    original_swagger = os.path.join(fileDirectory, constants.SWAGGER)
    generated_swagger = os.path.join(fileDirectory, constants.GENERATED_SWAGGER)
    warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)
    with open(original_swagger, 'r') as f1:
        with open(generated_swagger, 'r') as f2:
            loaded1 = yaml.load(f1)
            loaded2 = yaml.load(f2)
            compare_paths(loaded1, loaded2)
            compare_definitions(loaded1, loaded2)
            if len(global_issues) != 0:
                sys.exit(1)