#!/usr/bin/env python3
"""
Basic AWS CodeBuild build spec runner
"""

import io
import os
import glob
import subprocess
import tempfile
import zipfile
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def main():
    """
    Entrypoint

    Store alongside your buildspec.yml, run from the root of your project
    """
    buildspec_path = os.path.dirname(__file__)
    input_file = io.open(buildspec_path + '/buildspec.yml')
    buildspec = yaml.load(input_file, Loader=Loader)

    buildenv = os.environ
    for var in buildspec['env']['variables']:
        buildenv[var] = buildspec['env']['variables'][var]

    for command in buildspec['phases']['build']['commands']:
        process = subprocess.Popen(command, env=buildenv, shell=True)
        return_code = process.wait()
        if return_code != 0:
            exit(return_code)

    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    with zipfile.ZipFile(tmp_file.name, 'w') as output_zip:
        for file_glob in buildspec['artifacts']['files']:
            for file in glob.glob(file_glob):
                print('adding ' + file)
                output_zip.write(file, os.path.basename(file))

    print(tmp_file.name)

if __name__ == '__main__':
    main()
