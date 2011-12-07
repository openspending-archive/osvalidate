# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)


__all__ = ['TestCase']

class TestCase(object):

    def setup(self):
        pass

    def teardown(self):
        pass
