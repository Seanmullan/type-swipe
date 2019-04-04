import unittest
import sys
sys.path.append('data/')
import data
sys.path.append('tests/')

testModules = ['example_test']

suite = unittest.TestSuite()

for t in testModules:
    try:
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)
