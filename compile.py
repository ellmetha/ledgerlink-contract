"""

    Compiler helper
    ===============

    This modules simply imports the neo-boa `Compiler` abstraction and triggers the compilation of
    the contract whose filename is passed as first argument.

"""

import os
import sys

from boa.compiler import Compiler


path = sys.argv[1]
filename = os.path.basename(path)
Compiler.load_and_save(
    path,
    output_path=os.path.join(os.getcwd(), 'build', '{}.avm'.format(os.path.splitext(filename)[0])))
