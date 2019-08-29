##
# File:    ValidationReportProviderTests.py
# Author:  J. Westbrook
# Date:    3-Feb-2019
# Version: 0.001
#
# Update:
#
#
##
"""
Tests for provider of validation report extraction and translation utilities.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import unittest

from rcsb.utils.io.MarshalUtil import MarshalUtil
from rcsb.utils.validation.ValidationReportProvider import ValidationReportProvider

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()


class ValidationReportProviderTests(unittest.TestCase):
    def setUp(self):
        self.__dirPath = os.path.join(os.path.dirname(TOPDIR), "rcsb", "mock-data")
        self.__workPath = os.path.join(HERE, "test-output")
        self.__exampleFileXray = os.path.join(self.__dirPath, "MOCK_VALIDATION_REPORTS", "cb", "1cbs", "1cbs_validation.xml.gz")
        self.__cifFileXray = os.path.join(self.__workPath, "1cbs_validation.cif")
        self.__exampleFileNmr = os.path.join(self.__dirPath, "MOCK_VALIDATION_REPORTS", "dr", "6drg", "6drg_validation.xml.gz")
        self.__cifFileNmr = os.path.join(self.__workPath, "6drg_validation.cif")

    def tearDown(self):
        pass

    def testProviderReadValidationReport(self):
        mU = MarshalUtil()
        vpr = ValidationReportProvider(dirPath=os.path.join(self.__workPath, "vprt"), useCache=False, cleaCache=True)
        vrd = vpr.getReader()
        cL = mU.doImport(self.__exampleFileXray, fmt="xml", marshalHelper=vrd.toCif)
        ok = mU.doExport(self.__cifFileXray, cL, fmt="mmcif")
        self.assertTrue(ok)
        vpr = ValidationReportProvider(dirPath=os.path.join(self.__workPath, "vprt"), useCache=True, cleaCache=False)
        vrd = vpr.getReader()
        xrt = mU.doImport(self.__exampleFileNmr, fmt="xml")
        cL = vrd.toCif(xrt)
        ok = mU.doExport(self.__cifFileNmr, cL, fmt="mmcif")
        self.assertTrue(ok)


def providerReadValidationReport():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ValidationReportProviderTests("testProviderReadValidationReport"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = providerReadValidationReport()
    unittest.TextTestRunner(verbosity=2).run(mySuite)