#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from configparser_extended import ExtendedConfigParser


class BasicTestCase(unittest.TestCase):

    def test_basic(self):
        x = ExtendedConfigParser()
        self.assertTrue(x is not None)
