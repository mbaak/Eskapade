# **************************************************************************************
# * Project: Eskapade - A python-based package for data analysis                       *
# * Created : 2017-09-20                                                               *
# *                                                                                    *
# * Description:                                                                       *
# *      Helper functions for eskapade_bootstrap                                       *
# *                                                                                    *
# * Authors:                                                                           *
# *      KPMG Big Data team, Amstelveen, The Netherlands                               *
# *                                                                                    *
# * Redistribution and use in source and binary forms, with or without                 *
# * modification, are permitted according to the terms listed in the file              *
# * LICENSE.                                                                           *
# **************************************************************************************

import datetime
import os
import sys

from eskapade.logger import Logger

logger = Logger(__name__)


def get_absolute_path(path):
    """Get an absolute path.

    First expands ~ if present. Second take care of any . or ..

    :param path: path
    :returns: the absolute path
    """
    return os.path.abspath(os.path.expanduser(path))


def create_dir(path):
    """Create a leaf directory and all intermediate ones.

    Exit with a status code other than 0 if there is an error.

    :param path: an absolute path to the directory
    """
    try:
        logger.info('Creating the directory {dir!s}.', dir=path)
        os.makedirs(path, exist_ok=True)
    except PermissionError as exc:
        logger.error('Failed to create the directory {dir!s}! error={err!s}.', dir=path, err=exc.strerror)
        sys.exit(exc.errno)


def create_file(path, file_name, content=''):
    """Create a file in a given directory.

    Exit with a status code other than 0 if there is an error.

    :param path: an absolute path to the directory
    :param file_name: file name
    :param content: file's content
    :return path to created file
    """
    try:
        logger.info('Creating {file_name} in the directory {dir!s}.', file_name=file_name, dir=path)
        fp = open(path + '/' + file_name, 'w')
    except PermissionError as exc:
        logger.error('Failed to create {file_name} in the directory {dir!s}! error={err!s}.',
                     file_name=file_name, dir=path, err=exc.strerror)
        sys.exit(exc.errno)
    else:
        with fp:
            fp.write(content)


def generate_link(link_dir, link_name, is_create_init=False):
    """Generate Eskapade link.

    :param link_dir: absolute path to a directory where the link will be generated
    :param link_name: name of the link to generate
    :param is_create_init: whether to create __init__.py file or no
    """
    # Do not modify the indentation of template!
    template = """# **********************************************************************************
# * Project: Eskapade - A python-based package for data analysis                   *
# * Class  : {link_name!s}
# * Created: {date_generated!s}
# * Description:                                                                   *
# *      Algorithm to do...(fill in one-liner here)                                *
# *                                                                                *
# * Authors:                                                                       *
# *      KPMG Big Data team, Amstelveen, The Netherlands                           *
# *                                                                                *
# * Redistribution and use in source and binary forms, with or without             *
# * modification, are permitted according to the terms listed in the file          *
# * LICENSE.                                                                       *
# **********************************************************************************

from eskapade import process_manager, ConfigObject, DataStore, Link, StatusCode


class {link_name!s}(Link):

    \"\"\"Defines the content of link.\"\"\"

    def __init__(self, **kwargs):
        \"\"\"Initialize an instance.

        :param str name: name of link
        :param str read_key: key of input data to read from data store
        :param str store_key: key of output data to store in data store
        \"\"\"
        # initialize Link, pass name from kwargs
        Link.__init__(self, kwargs.pop('name', '{link_name!s}'))

        # Process and register keyword arguments.  All arguments are popped from
        # kwargs and added as attributes of the link.  The values provided here
        # are defaults.
        self._process_kwargs(kwargs, read_key=None, store_key=None)

        # check residual kwargs; exit if any present
        self.check_extra_kwargs(kwargs)
        # Turn off line above, and on two lines below if you wish to keep these
        # extra kwargs.
        #self.kwargs = kwargs

    def initialize(self):
        \"\"\"Initialize the link.

        :returns: status code of initialization
        :rtype: StatusCode
        \"\"\"
        return StatusCode.Success

    def execute(self):
        \"\"\"Execute the link.

        :returns: status code of execution
        :rtype: StatusCode
        \"\"\"
        settings = process_manager.service(ConfigObject)
        ds = process_manager.service(DataStore)

        # --- your algorithm code goes here

        self.logger.debug('Now executing link: {{link}}', link=self.name)
        return StatusCode.Success

    def finalize(self):
        \"\"\"Finalize the link.

        :returns: status code of finalization
        :rtype: StatusCode
        \"\"\"
        # --- any code to finalize the link follows here

        return StatusCode.Success
"""
    file_name = link_name.lower()

    import_line = 'from .{file_name} import {link_name}'.format(file_name=file_name, link_name=link_name)
    create_file(path=link_dir,
                file_name='{file_name!s}.py'.format(file_name=file_name),
                content=template.format(link_name=link_name, date_generated=datetime.date.today()))
    if is_create_init:
        init_content = '# Created by Eskapade on {date!s}\n{import_line}\n'.format(date=datetime.date.today(),
                                                                                   import_line=import_line)
        create_file(path=link_dir,
                    file_name='__init__.py',
                    content=init_content)
    else:
        logger.info('Edit {link_dir}/__init__.py: add \"{link_name}\" to __all__ and add the line "{import_line}".'
                    .format(link_dir=link_dir, file_name=file_name, link_name=link_name, import_line=import_line))


def generate_macro(macro_dir, macro_name, link_module='eskapade.core_ops', link_name='HelloWorld',
                   is_create_init=False):
    """Generate Eskapade macro.

    :param macro_dir: absolute path to a directory where the macro will be generated
    :param macro_name: name of the macro to generate
    :param link_module: module of a link to import
    :param link_name: name of the link to import
    :param is_create_init: whether to create __init__.py file or no
    """
    # Do not modify the indentation of template!
    template = """# **********************************************************************************
# * Project: Eskapade - A python-based package for data analysis                   *
# * Macro  : {macro_name!s}
# * Created: {date_generated!s}
# * Description:                                                                   *
# *      Macro do...(fill in short description here)                               *
# *                                                                                *
# * Authors:                                                                       *
# *      Your name(s) here                                                         *
# *                                                                                *
# * Redistribution and use in source and binary forms, with or without             *
# * modification, are permitted according to the terms listed in the file          *
# * LICENSE.                                                                       *
# **********************************************************************************

from eskapade import process_manager, ConfigObject
from eskapade.logger import Logger, LogLevel

from {link_module!s} import {link_name!s}

logger = Logger()

logger.debug('Now parsing configuration file {macro_name!s}.')

# --- minimal analysis information

settings = process_manager.service(ConfigObject)
settings['analysisName'] = '{macro_name!s}'
settings['version'] = 0

# --- now set up the chains and links

ch = process_manager.add_chain('Start')
link = {link_name!s}()
link.logger.log_level = LogLevel.DEBUG
ch.add_link(link)

logger.debug('Done parsing configuration file {macro_name!s}.')
"""

    content = template.format(macro_name=macro_name,
                              date_generated=datetime.date.today(),
                              link_module=link_module,
                              link_name=link_name)
    if is_create_init:
        init_content = '# Created by Eskapade on {date!s}\n' \
                       'from {link_module}.links import *\n'.format(link_module=link_module,
                                                                    date=datetime.date.today())
        create_file(path=macro_dir,
                    file_name='__init__.py',
                    content=init_content)
    create_file(path=macro_dir,
                file_name='{macro_name!s}.py'.format(macro_name=macro_name),
                content=content)


def generate_notebook(notebook_dir, notebook_name, macro_path=None):
    """Generate Eskapade notebook.

    :param notebook_dir: absolute path to a directory where the notebook will be generated
    :param notebook_name: name of the notebook to generate
    :param macro_path: absolute path to a macro the notebook executes
    """
    import platform

    from eskapade import resources

    if macro_path:
        macro_path = "'{path}'".format(path=macro_path)
    else:
        macro_path = "resources.tutorial('tutorial_1.py')"

    with open(resources.template('notebook_template.ipynb')) as file:
        template = file.read()
        content = template.format(macro_path=macro_path,
                                  analysis_name=notebook_name,
                                  python_version=platform.python_version())
        create_file(path=notebook_dir,
                    file_name='{notebook_name!s}.ipynb'.format(notebook_name=notebook_name),
                    content=content)


def generate_setup(root_dir, project_name):
    """Generate project's setup.py.

    :param root_dir: absolute path to an analysis project root dir
    :param project_name: project's name
    """
    # Do not modify the indentation of template!
    template = """from setuptools import setup, find_packages

NAME = '{project_name}'


def setup_package() -> None:
    \"\"\"
    The main setup method. It is responsible for setting up and installing the package.
    \"\"\"
    setup(name=NAME,
          python_requires='>=3.5',
          package_dir={{'': '.'}},
          packages=find_packages(),
          install_requires=['eskapade']
          )


if __name__ == '__main__':
    setup_package()
"""
    content = template.format(project_name=project_name)
    create_file(path=root_dir, file_name='setup.py', content=content)