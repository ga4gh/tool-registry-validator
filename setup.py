from setuptools import setup

setup(name='ga4gh-tool-registry-validate',
      version='1.0',
      description='Client tool for GA4GH tool registry api',
      author='GA4GH Data working group containers and workflows task team',
      author_email='',
      url="",
      download_url="",
      license='Apache 2.0',
      packages=["ga4gh_tool_registry"],
      install_requires=['cwltool==1.0.20180403145700', 'Flask', 'ruamel.yaml==0.14.12',
                        'schema-salad==2.7.20180514132321', 'avro==1.8.1', 'setuptools==65.5.1', 'requests==2.18.4'],
      test_suite='tests',
      tests_require=[],
      zip_safe=True,
      entry_points={
          'console_scripts': ["ga4gh-tool-registry-validate=ga4gh_tool_registry.validate:main"]
      }
      )
