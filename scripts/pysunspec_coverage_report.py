import coverage
import os
import unittest

# Start the coverage.py tracking
cov = coverage.Coverage()
cov.start()

# Find the top_level sunspec path
scripts_dir = os.path.abspath(os.path.dirname(__file__))  # scripts/
pysunspec_top = os.path.split(scripts_dir)[0]  # ../
sunspec_dir = os.path.join(pysunspec_top, 'sunspec')

# Find and run all of the tests in the repository
loader = unittest.TestLoader()
package_tests = loader.discover(sunspec_dir)
runner = unittest.TextTestRunner()
for test in package_tests:
    runner.run(test)

# End the coverage.py tracking and make an html report. The html report can be
# viewed in the folder this code was run by opening htmlcov/index.html
cov.stop()
cov.save()
cov.html_report()
