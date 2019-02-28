#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

package_info = generate_distutils_setup()
package_info['packages'] = ['py_model_tools']
package_info['package_dir'] = {'': 'src'}
package_info['install_requires'] = []
package_info['scrips'] = ['nodes']

setup(**package_info)
