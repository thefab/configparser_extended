#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from configparser import NoOptionError, NoSectionError
from configparser_extended import ExtendedConfigParser
from collections import OrderedDict


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.x = ExtendedConfigParser()
        self.x.read('./test_cfg.ini')

    def test_basic(self):
        self.assertTrue(self.x is not None)

    def test_get_basic(self):
        self.assertEqual(self.x.get('sect2', 'key2'), 'val2')

    def test_get_basic_fail(self):
        self.assertRaises(NoOptionError, self.x.get, 'sect2', 'key4')

    def test_get_basic_fail2(self):
        self.assertRaises(NoSectionError, self.x.get, 'sect4', 'key3')

    def test_get_int(self):
        self.assertEqual(self.x.getint('sect1', 'key_int'), 1)

    def test_get_float(self):
        self.assertEqual(self.x.getfloat('sect1', 'key_float'), 1.24)

    def test_get_boolean_true(self):
        self.assertTrue(self.x.getboolean('sect1', 'key_bool1'))

    def test_get_boolean_on(self):
        self.assertTrue(self.x.getboolean('sect1', 'key_bool2'))

    def test_get_boolean_1(self):
        self.assertTrue(self.x.getboolean('sect1', 'key_bool3'))

    def test_get_boolean_yes(self):
        self.assertTrue(self.x.getboolean('sect1', 'key_bool4'))

    def test_get_boolean_false(self):
        self.assertFalse(self.x.getboolean('sect1', 'key_bool5'))

    def test_get_boolean_random(self):
        self.assertFalse(self.x.getboolean('sect1', 'key_bool6'))

    def test_default(self):
        self.assertEqual(self.x.get('sect3', 'key2'), 'default2')

    def test_default_section(self):
        default = OrderedDict([('key2', 'default2'), ('key3', 'default3'),
                              ('key049', 'DEFAULT')])
        self.assertEqual(self.x.default_section, default)

    def test_get_vars(self):
        self.assertEqual(self.x.get('sect1', 'key1', vars={'key1': 'deez'}),
                         'deez')

    def test_get_fallback(self):
        self.assertEqual(self.x.get('sect1', 'key173', fallback='deez'),
                         'deez')

    def test_has_section(self):
        self.assertTrue(self.x.has_section('sect2'))

    def test_has_section_advanced(self):
        self.assertTrue(self.x.has_section('sect1'))

    def test_has_section_fail(self):
        self.assertFalse(self.x.has_section('sect42'))

    def test_has_option(self):
        self.assertTrue(self.x.has_option('sect3', 'key3'))

    def test_has_option_inheritance(self):
        self.assertTrue(self.x.has_option('sect1', 'key3'))

    def test_has_option_advanced_fail(self):
        # Because config dependant
        self.assertFalse(self.x.has_option('sect3', 'key2'))

    def test_has_option_fail(self):
        self.assertFalse(self.x.has_option('sect3', 'key4'))

    def test_has_option_strict(self):
        self.assertTrue(self.x.has_option_strict('sect3', 'key3'))

    def test_has_option_strict_inheritance(self):
        # Because strict
        self.assertFalse(self.x.has_option_strict('sect1', 'key3'))

    def test_has_option_strict_advanced_fail(self):
        # Because config dependant
        self.assertFalse(self.x.has_option_strict('sect3', 'key2'))

    def test_has_option_strict_fail(self):
        self.assertFalse(self.x.has_option_strict('sect3', 'key4'))

    def test_has_option_config_ind(self):
        self.assertTrue(self.x.has_option_config_ind('sect3', 'key3'))

    def test_has_option_config_ind_inheritance(self):
        self.assertTrue(self.x.has_option_config_ind('sect1', 'key3'))

    def test_has_option_config_ind_advanced(self):
        self.assertTrue(self.x.has_option_config_ind('sect3', 'key2'))

    def test_has_option_config_ind_fail(self):
        self.assertFalse(self.x.has_option_config_ind('sect3', 'key4'))

    def test_has_option_strict_config_ind(self):
        self.assertTrue(self.x.has_option_strict_config_ind('sect3', 'key3'))

    def test_has_option_strict_config_ind_inheritance(self):
        self.assertFalse(self.x.has_option_strict_config_ind('sect1', 'key3'))

    def test_has_option_strict_config_ind_advanced(self):
        self.assertTrue(self.x.has_option_strict_config_ind('sect3', 'key2'))

    def test_has_option_strict_config_ind_fail(self):
        self.assertFalse(self.x.has_option_strict_config_ind('sect3', 'key4'))

    def test_get_key_dict(self):
        self.assertEqual(self.x['sect2']['key2'], 'val2')

    def test_get_sect_dict_fail(self):
        self.assertRaises(KeyError, lambda: self.x['sect4'])

    def test_get_key_dict_fail(self):
        self.assertRaises(KeyError, lambda: self.x['sect2']['key42'])


class AdvancedTestCase(unittest.TestCase):

    def setUp(self):
        self.x = ExtendedConfigParser()
        self.x.read('./test_cfg.ini')

    def test_get_list(self):
        res = ['damn', 'dang', 'nabbit']
        self.assertEqual(self.x.get('sect1', 'key_list'), res)

    def test_get_list_int(self):
        res = [1, 7, 3]
        self.assertEqual(self.x.getint('sect1', 'key_list_int'), res)

    def test_get_list_bool(self):
        res = [True, False, True]
        self.assertEqual(self.x.getboolean('sect1', 'key_list_bool'), res)

    def test_get_list_float(self):
        res = [0.96, 1.73, 6.82]
        self.assertEqual(self.x.getfloat('sect1', 'key_list_float'), res)

    def test_get_father(self):
        self.x = ExtendedConfigParser(defaults={'key4': 'father'})
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect1', 'key4'), 'father')

    def test_get_default_over_father(self):
        self.x = ExtendedConfigParser(defaults={'key049': 'father'})
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect1', 'key049'), 'DEFAULT')


class InheritanceTestCase(unittest.TestCase):

    def setUp(self):
        self.x = ExtendedConfigParser()
        self.x.read('./test_cfg.ini')

    def test_get_section_name(self):
        self.assertEqual(self.x.get_section_name('sect1'), 'sect1:sect2:sect3')

    def test_get_section_name_fail(self):
        self.assertRaises(NoSectionError, self.x.get_section_name, 'sect4')

    def test_get_basic2(self):
        self.assertEqual(self.x.get('sect1', 'key1'), 'val1')

    def test_get_basic_fail2(self):
        self.assertRaises(NoOptionError, self.x.get, 'sect1', 'key412')

    def test_get_sections(self):
        sections = ['sect1:sect2:sect3', 'sect2', 'sect3']
        self.assertEqual(self.x.get_corresponding_sections('sect1'), sections)

    def test_get_parent_key(self):
        self.assertEqual(self.x.get('sect1', 'key2'), 'val2')

    def test_get_grandparent_key(self):
        self.assertEqual(self.x.get('sect1', 'key3'), 'val3')

    def test_get_key_dict(self):
        self.assertEqual(self.x['sect1']['key1'], 'val1')

    def test_get_parent_key_dict(self):
        self.assertEqual(self.x['sect1']['key2'], 'val2')

    def test_get_grandparent_key_dict(self):
        self.assertEqual(self.x['sect1']['key3'], 'val3')

    def test_get_key_dict_fail(self):
        self.assertRaises(KeyError, lambda: self.x['sect2']['key4'])

    def test_get_sect_dict_fail(self):
        self.assertRaises(KeyError, lambda: self.x['sect42']['key1'])


class SpecificationTestCase(unittest.TestCase):

    def setUp(self):
        self.x = ExtendedConfigParser(config='dev')
        self.x.read('./test_cfg.ini')

    def test_specification_basic(self):
        self.assertEqual(self.x.get('sect1', 'key1'), 'dev1')

    def test_specification_goto_parent_config(self):
        self.x.set_config_name('dev_stuff')
        self.assertEqual(self.x.get('sect1', 'key1'), 'dev1')

    def test_specification_goto_grandparent(self):
        self.x.set_config_name('dev_dem_der')
        self.assertEqual(self.x.get('sect1', 'key1'), 'dev1')

    def test_get_configs(self):
        self.x.set_config_name('dev_plop_toto')
        res = ['dev_plop_toto', 'dev_plop', 'dev']
        self.assertEqual(self.x.get_configs(), res)

    def test_get_configs_plus(self):
        self.x.set_config_name('dev_plop_toto')
        res = ['dev_plop_toto', 'plop_toto', 'toto', 'dev_plop', 'plop', 'dev']
        self.assertEqual(self.x.get_configs_plus(), res)

    def test_specification_advanced(self):
        self.x.set_config_name('dev_plop_toto')
        self.assertEqual(self.x.get('sect3', 'key3'), 'dev_plop_toto3')
