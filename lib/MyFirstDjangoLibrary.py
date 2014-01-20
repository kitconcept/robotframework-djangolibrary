"""A library for *documentation format* demonstration purposes.

This documentation is created using reStructuredText__. Here is a link
to the only \\`Keyword\\`.

__ http://docutils.sourceforge.net
"""

ROBOT_LIBRARY_DOC_FORMAT = 'reST'


class MyFirstDjangoLibrary:

    # TEST CASE => New instance is created for every test case.
    # TEST SUITE => New instance is created for every test suite.
    # GLOBAL => Only one instance is created during the whole test execution.
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, host="127.0.0.1", port=8000):
        print("INIT")

    def start_django(self):
        """**Nothing** to see here. Not even in the table below.

        =======  =====  =====
        Table    here   has
        nothing  to     see.
        =======  =====  =====
        """
        print("START DJANGO")

    def stop_django(self):
        print("STOP DJANGO")

    def my_keyword(self):
        print('Hello, world!')
