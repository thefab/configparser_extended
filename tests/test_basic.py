#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from configparser import NoOptionError, NoSectionError
from configparser_extended import ExtendedConfigParser, SectionProxyExtended
try:
    from backports.configparser.helpers import OrderedDict
except ImportError:
    from collections import OrderedDict
from six import u


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
        self.assertRaises(NoSectionError, self.x.get, 'sect404', 'key3')

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
        self.assertRaises(ValueError, self.x.getboolean, 'sect1', 'key_bool6')

    def test_default(self):
        self.assertEqual(self.x.get('sect3', 'key2'), 'default2')

    def test_default_section(self):
        default = OrderedDict([('key1[dev_plop_toto_stuff]',
                                'dev_plop_toto1_default'),
                              ('key2', 'default2'), ('key3', 'default3'),
                              ('key049', 'DEFAULT'),
                              ('key049[dev]', 'DEFAULT_dev')])
        self.assertEqual(self.x.default_section, default)

    def test_get_vars(self):
        self.assertEqual(self.x.get('sect1', 'key1', vars={'key1': 'deez'}),
                         'deez')

    def test_get_fallback(self):
        self.assertEqual(self.x.get('sect1', 'key173', fallback='deez'),
                         'deez')

    def test_get_fallback_None(self):
        self.assertEqual(self.x.get('sect1', 'key173', fallback=None), None)

    def test_get_fallback_no_section(self):
        x = ExtendedConfigParser(config="FOO", strict=False)
        x.read('./test_cfg.ini')
        self.assertEqual(x.get('sect_does_not_exsist', 'key173',
                               fallback='deez'), 'deez')

    def test_get_fallback_no_section_None(self):
        x = ExtendedConfigParser(config="FOO", strict=False)
        x.read('./test_cfg.ini')
        self.assertEqual(x.get('sect_does_not_exsist', 'key173',
                               fallback=None), None)

    def test_has_section(self):
        self.assertTrue(self.x.has_section('sect2'))

    def test_has_section_advanced(self):
        self.assertTrue(self.x.has_section('sect1'))

    def test_has_section_fail(self):
        self.assertFalse(self.x.has_section('sect404'))

    def test_has_option(self):
        self.assertTrue(self.x.has_option('sect3', 'key3'))

    def test_has_option_config(self):
        self.assertTrue(self.x.has_option('sect3', 'key2', 'dev'))

    def test_has_option_config_fail(self):
        self.assertFalse(self.x.has_option('sect3', 'key2', 'scp'))

    def test_has_option_inheritance(self):
        self.assertTrue(self.x.has_option('sect1', 'key3'))

    def test_has_option_specificaction_fail(self):
        # Because config dependant
        self.assertFalse(self.x.has_option('sect3', 'key2'))

    def test_has_option_fail(self):
        self.assertFalse(self.x.has_option('sect3', 'key4'))

    def test_has_option_strict(self):
        self.assertTrue(self.x.has_option('sect3', 'key3', strict=True))

    def test_has_option_strict_config(self):
        self.assertTrue(self.x.has_option('sect3', 'key2', 'dev', strict=True))

    def test_has_option_strict_config_fail(self):
        self.assertFalse(self.x.has_option('sect3', 'key2', 'scp',
                                           strict=True))

    def test_has_option_strict_inheritance(self):
        # Because strict
        self.assertFalse(self.x.has_option('sect1', 'key3', strict=True))

    def test_has_option_strict_specificaction_fail(self):
        # Because config dependant
        self.assertFalse(self.x.has_option('sect3', 'key2', strict=True))

    def test_has_option_strict_fail(self):
        self.assertFalse(self.x.has_option('sect3', 'key4', strict=True))

    def test_has_option_config_ind(self):
        self.assertTrue(self.x.has_option('sect3', 'key3', cfg_ind=True))

    def test_has_option_config_ind_inheritance(self):
        self.assertTrue(self.x.has_option('sect1', 'key3', cfg_ind=True))

    def test_has_option_config_ind_specificaction(self):
        self.assertTrue(self.x.has_option('sect3', 'key2', cfg_ind=True))

    def test_has_option_config_ind_fail(self):
        self.assertFalse(self.x.has_option('sect3', 'key4', cfg_ind=True))

    def test_has_option_strict_config_ind(self):
        self.assertTrue(self.x.has_option('sect3', 'key3', cfg_ind=True,
                                          strict=True))

    def test_has_option_strict_config_ind_inheritance(self):
        self.assertFalse(self.x.has_option('sect1', 'key3', cfg_ind=True,
                                           strict=True))

    def test_has_option_strict_config_ind_specificaction(self):
        self.assertTrue(self.x.has_option('sect3', 'key2', cfg_ind=True,
                                          strict=True))

    def test_has_option_strict_config_ind_fail(self):
        self.assertFalse(self.x.has_option('sect3', 'key4', cfg_ind=True,
                                           strict=True))

    def test_options_basic(self):
        res = ['key1', 'key2', 'key2[dev]', 'key2[dev_plop]',
               'key1[dev_plop_toto_stuff]', 'key2', 'key3', 'key049',
               'key049[dev]']
        self.assertEquals(self.x.options('sect2'), res)

    def test_options_inheritance(self):
        res = ['key1', 'key_int', 'key_bool1', 'key_bool2', 'key_bool3',
               'key_bool4', 'key_bool5', 'key_bool6', 'key_float', 'key_list',
               'key_list_int', 'key_list_bool', 'key_list_float', 'key1[dev]',
               'key1', 'key2', 'key2[dev]', 'key2[dev_plop]',
               'key1[dev_plop_toto]', 'key2[dev]', 'key3', 'key3[dev]',
               'key3[toto]', 'key3[dev_plop]', 'key3[dev_plop_toto]',
               'key1[dev_plop_toto_stuff]', 'key2', 'key3', 'key049',
               'key049[dev]']
        self.assertEquals(self.x.options('sect1'), res)

    def test_options_strict(self):
        res = ['key1', 'key_int', 'key_bool1', 'key_bool2', 'key_bool3',
               'key_bool4', 'key_bool5', 'key_bool6', 'key_float', 'key_list',
               'key_list_int', 'key_list_bool', 'key_list_float', 'key1[dev]']
        self.assertEquals(self.x.options('sect1', strict=True), res)

    def test_options_strict_defaults(self):
        res = ['key1', 'key_int', 'key_bool1', 'key_bool2', 'key_bool3',
               'key_bool4', 'key_bool5', 'key_bool6', 'key_float', 'key_list',
               'key_list_int', 'key_list_bool', 'key_list_float', 'key1[dev]',
               'key1[dev_plop_toto_stuff]', 'key2', 'key3', 'key049',
               'key049[dev]']
        self.assertEquals(self.x.options('sect1', strict=True, defaults=True),
                          res)

    def test_options_strict_config_ind(self):
        res = ['key1', 'key_int', 'key_bool1', 'key_bool2', 'key_bool3',
               'key_bool4', 'key_bool5', 'key_bool6', 'key_float', 'key_list',
               'key_list_int', 'key_list_bool', 'key_list_float']
        self.assertEquals(self.x.options('sect1', strict=True, cfg_ind=True),
                          res)

    def test_options_strict_config_ind_defaults(self):
        res = ['key1', 'key_int', 'key_bool1', 'key_bool2', 'key_bool3',
               'key_bool4', 'key_bool5', 'key_bool6', 'key_float', 'key_list',
               'key_list_int', 'key_list_bool', 'key_list_float', 'key2',
               'key3', 'key049']
        self.assertEquals(self.x.options('sect1', strict=True, defaults=True,
                          cfg_ind=True), res)

    def test_options_config_ind(self):
        res = ['key1', 'key_int', 'key_bool1', 'key_bool2', 'key_bool3',
               'key_bool4', 'key_bool5', 'key_bool6', 'key_float', 'key_list',
               'key_list_int', 'key_list_bool', 'key_list_float',
               'key2', 'key3', 'key049']
        self.assertEquals(self.x.options('sect1', cfg_ind=True).sort(),
                          res.sort())

    def test_items_basic(self):
        res = [('key1', 'val1_sect2'),
               ('key2', 'val2'),
               ('key2[dev]', 'dev2'),
               ('key2[dev_plop]', 'dev_plop2'),
               ('key1[dev_plop_toto_stuff]', 'dev_plop_toto1_default'),
               ('key2', 'default2'),
               ('key3', 'default3'),
               ('key049', 'DEFAULT'),
               ('key049[dev]', 'DEFAULT_dev')]
        res.sort()
        test = self.x.items('sect2')
        test.sort()
        self.assertEquals(test, res)

    def test_items_inheritance(self):
        res = [('key1', 'val1'),
               ('key_int', '1'),
               ('key_bool1', 'true'),
               ('key_bool2', 'on'),
               ('key_bool3', '1'),
               ('key_bool4', 'yes'),
               ('key_bool5', 'false'),
               ('key_bool6', 'random'),
               ('key_float', '1.24'),
               ('key_list', 'damn;dang;nabbit'),
               ('key_list_int', '1;7;3'),
               ('key_list_bool', 'true;false;true'),
               ('key_list_float', '0.96;1.73;6.82'),
               ('key1[dev]', 'dev1'),
               ('key1', 'val1_sect2'),
               ('key2', 'val2'),
               ('key2[dev]', 'dev2'),
               ('key2[dev_plop]', 'dev_plop2'),
               ('key1[dev_plop_toto]', 'dev_plop_toto1_sect3'),
               ('key2[dev]', 'dev2_sect3'),
               ('key3', 'val3'),
               ('key3[dev]', 'dev3'),
               ('key3[toto]', 'toto3'),
               ('key3[dev_plop]', 'dev_plop3'),
               ('key3[dev_plop_toto]', 'dev_plop_toto3'),
               ('key1[dev_plop_toto_stuff]', 'dev_plop_toto1_default'),
               ('key2', 'default2'),
               ('key3', 'default3'),
               ('key049', 'DEFAULT'),
               ('key049[dev]', 'DEFAULT_dev')]
        res.sort()
        test = self.x.items('sect1')
        test.sort()
        self.assertEquals(test, res)

    def test_items_strict_basic(self):
        res = [('key1', 'val1'),
               ('key_int', '1'),
               ('key_bool1', 'true'),
               ('key_bool2', 'on'),
               ('key_bool3', '1'),
               ('key_bool4', 'yes'),
               ('key_bool5', 'false'),
               ('key_bool6', 'random'),
               ('key_float', '1.24'),
               ('key_list', 'damn;dang;nabbit'),
               ('key_list_int', '1;7;3'),
               ('key_list_bool', 'true;false;true'),
               ('key_list_float', '0.96;1.73;6.82'),
               ('key1[dev]', 'dev1')]
        res.sort()
        test = self.x.items('sect1', strict=True)
        test.sort()
        self.assertEquals(test, res)

    def test_items_strict_defaults(self):
        res = [('key1', 'val1'),
               ('key_int', '1'),
               ('key_bool1', 'true'),
               ('key_bool2', 'on'),
               ('key_bool3', '1'),
               ('key_bool4', 'yes'),
               ('key_bool5', 'false'),
               ('key_bool6', 'random'),
               ('key_float', '1.24'),
               ('key_list', 'damn;dang;nabbit'),
               ('key_list_int', '1;7;3'),
               ('key_list_bool', 'true;false;true'),
               ('key_list_float', '0.96;1.73;6.82'),
               ('key1[dev]', 'dev1'),
               ('key1[dev_plop_toto_stuff]', 'dev_plop_toto1_default'),
               ('key2', 'default2'),
               ('key3', 'default3'),
               ('key049', 'DEFAULT'),
               ('key049[dev]', 'DEFAULT_dev')]
        res.sort()
        test = self.x.items('sect1', defaults=True, strict=True)
        test.sort()
        self.assertEquals(test, res)

    def test_items_all(self):
        res = []
        for key in self.x._sections:
            res.append((key, SectionProxyExtended(self.x, key)))
        res.sort()
        test = self.x.items()
        test.sort()
        self.assertEquals(test, res)

    def test_items_strict_all(self):
        res = []
        for key in self.x._sections:
            res.append((key, SectionProxyExtended(self.x, key)))
        res.sort()
        test = self.x.items(strict=True)
        test.sort()
        self.assertEquals(test, res)

    def test_items_vars(self):
        res = [('william', 'Overbeck'),
               ('key1', 'val1_sect2'),
               ('key2', 'val2'),
               ('key2[dev]', 'dev2'),
               ('key2[dev_plop]', 'dev_plop2'),
               ('key1[dev_plop_toto_stuff]', 'dev_plop_toto1_default'),
               ('key2', 'default2'),
               ('key3', 'default3'),
               ('key049', 'DEFAULT'),
               ('key049[dev]', 'DEFAULT_dev')]
        res.sort()
        test = self.x.items('sect2', vars={'William': 'Overbeck'})
        test.sort()
        self.assertEquals(test, res)

    def test_items_vars_strict(self):
        res = [('william', 'Overbeck'),
               ('key1', 'val1_sect2'),
               ('key2', 'val2'),
               ('key2[dev]', 'dev2'),
               ('key2[dev_plop]', 'dev_plop2')]
        res.sort()
        test = self.x.items('sect2', vars={'William': 'Overbeck'}, strict=True)
        test.sort()
        self.assertEquals(test, res)

    def test_get_key_dict(self):
        self.assertEqual(self.x['sect2']['key2'], 'val2')

    def test_get_sect_dict_fail(self):
        self.assertRaises(KeyError, lambda: self.x['sect404'])

    def test_get_key_dict_fail(self):
        self.assertRaises(KeyError, lambda: self.x['sect2']['key42'])

    def test_has_section_strict(self):
        self.assertTrue(self.x.has_section('sect2', strict=True))

    def test_has_section_strict_fail(self):
        self.assertFalse(self.x.has_section('sect1', strict=True))

    def test_defaults(self):
        self.x = ExtendedConfigParser(defaults={'william': 'Overbeck'})
        self.x.read('./test_cfg.ini')
        res = OrderedDict([('william', 'Overbeck')])
        self.assertEquals(self.x.defaults(), res)

    def test_add_section(self):
        self.x.add_section('Jim Hoxworth')
        self.assertTrue(self.x.has_section('Jim Hoxworth'))
        self.assertEqual(self.x.get('Jim Hoxworth', 'key2'), 'default2')
        self.assertEqual(self.x['Jim Hoxworth']['key2'], 'default2')

    def test_read_file(self):
        self.x = ExtendedConfigParser()
        data = open('./test_cfg.ini', 'r')
        self.x.read_file(data)
        self.assertEqual(self.x.get('sect2', 'key2'), 'val2')

    def test_read_string_unicode(self):
        self.x = ExtendedConfigParser()
        with open('./test_cfg.ini', 'r') as cfg_file:
            string = cfg_file.read()
        string = u(string)
        self.x.read_string(string)
        self.assertEqual(self.x.get('sect2', 'key2'), 'val2')


class AdvancedTestCase(unittest.TestCase):

    def setUp(self):
        self.x = ExtendedConfigParser()
        self.x.read('./test_cfg.ini')

    def test_get_not_list(self):
        res = 'damn;dang;nabbit'
        self.assertEqual(self.x.get('sect1', 'key_list'), res)

    def test_get_list(self):
        res = ['damn', 'dang', 'nabbit']
        self.assertEqual(self.x.get('sect1', 'key_list', isList=True), res)

    def test_get_list_int(self):
        res = [1, 7, 3]
        self.assertEqual(self.x.getintlist('sect1', 'key_list_int'), res)

    def test_get_list_bool(self):
        res = [True, False, True]
        self.assertEqual(self.x.getbooleanlist('sect1', 'key_list_bool'), res)

    def test_get_list_float(self):
        res = [0.96, 1.73, 6.82]
        self.assertEqual(self.x.getfloatlist('sect1', 'key_list_float'), res)

    def test_get_fallback_list(self):
        # If not found in the section or parents (tests list for defaults,
        # fallback, father,...)
        self.assertEqual(self.x.get('sect1', 'key173', fallback='deez',
                                    isList=True), ['deez'])

    def test_get_father(self):
        self.x = ExtendedConfigParser(defaults={'key4': 'father'})
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect1', 'key4'), 'father')

    def test_get_default_over_father(self):
        self.x = ExtendedConfigParser(defaults={'key049': 'father'})
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect1', 'key049'), 'DEFAULT')

    def test_get_config_plus(self):
        self.x = ExtendedConfigParser(config='mem_plop_toto')
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect3', 'key3', cfg_plus=True), 'toto3')

    def test_get_config_section_loop_basic(self):
        self.x = ExtendedConfigParser(config='dev_plop_toto')
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect1', 'key1', sect_first=False),
                         'dev_plop_toto1_sect3')

    def test_get_config_section_loop_default(self):
        self.x = ExtendedConfigParser(config='dev_plop_toto_stuff')
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect1', 'key1', sect_first=False),
                         'dev_plop_toto1_default')

    def test_get_config_section_loop_father(self):
        self.x = ExtendedConfigParser(config='dev_plop_toto_stuff',
                                      defaults={'key049[dev_plop]': 'father'})
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect1', 'key049', sect_first=False),
                         'father')

    def test_get_config_section_loop_vars_specified(self):
        self.x = ExtendedConfigParser(config='dev_plop_toto_stuff')
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect1', 'key1', sect_first=False,
                                    vars={'key1[dev_plop_toto_stuff]':
                                          'vars'}), 'vars')

    def test_get_config_section_loop_vars(self):
        self.x = ExtendedConfigParser(config='mem_plop_toto_stuff')
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect2', 'key1', sect_first=False,
                                    vars={'key1': 'vars'}), 'vars')

    def test_get_config_section_loop_vars_unspecified(self):
        self.x = ExtendedConfigParser()
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect2', 'key1', sect_first=False,
                                    vars={'key1': 'vars'}), 'vars')

    def test_get_config_section_loop_sect_unspecified(self):
        self.x = ExtendedConfigParser(config='dev_plop')
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect2', 'key1', sect_first=False),
                         'val1_sect2')

    def test_get_config_section_loop_default_unspecified(self):
        self.x = ExtendedConfigParser(config='mem_plop')
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect2', 'key049', sect_first=False),
                         'DEFAULT')

    def test_get_config_section_loop_father_unspecified(self):
        self.x = ExtendedConfigParser(config='mem_plop', defaults={'key096':
                                                                   'father'})
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect2', 'key096', sect_first=False),
                         'father')

    def test_get_config_section_loop_fallback(self):
        self.assertEqual(self.x.get('sect2', 'key173', sect_first=False,
                                    fallback='SCP-173'), 'SCP-173')

    def test_get_config_section_loop_fail(self):
        self.assertRaises(NoOptionError, self.x.get, 'sect1', 'key682',
                          sect_first=False)

    def test_get_config_section_loop_config_plus(self):
        self.x = ExtendedConfigParser(config='mem_plop_toto')
        self.x.read('./test_cfg.ini')
        self.assertEqual(self.x.get('sect3', 'key3', sect_first=False,
                         cfg_plus=True), 'toto3')

    def test_get_config_section_loop_list(self):
        self.assertEqual(self.x.get('sect2', 'key173', sect_first=False,
                                    fallback='SCP-173', isList=True),
                         ['SCP-173'])

    def test_get_kwargs(self):
        self.x = ExtendedConfigParser(config='dev',
                                      config_separator='#',
                                      section_separator='%',
                                      list_separator='*',
                                      delimiters=':',
                                      comment_prefixes=('#', ';'),
                                      inline_comment_prefixes=None,
                                      strict=True,
                                      empty_lines_in_values=True,
                                      default_section='THINGY',
                                      interpolation=None)
        self.x.read('./test_cfg_kwargs.ini')
        self.assertEqual(self.x.get('sect1', 'key2', isList=True),
                         ['dev2', '2ved', '2vedev2'])

    def test_set_config_separator(self):
        self.x = ExtendedConfigParser(config='dev#dem#der',
                                      section_separator='%',
                                      list_separator='*')
        self.x.read('./test_cfg_kwargs.ini')
        self.x.set_config_separator('#')
        self.assertEqual(self.x.get('sect1', 'key1'), 'dev1')

    def test_set_config_separator_wrong(self):
        self.x = ExtendedConfigParser(config='dev_dem_der',
                                      section_separator='%',
                                      list_separator='*')
        self.x.read('./test_cfg_kwargs.ini')
        self.x.set_config_separator('#')
        self.x.set_config_name('dev_dem_der')
        self.assertEqual(self.x.get('sect1', 'key1'), 'val1')

    def test_set_section_separator(self):
        self.x = ExtendedConfigParser(config='',
                                      config_separator='#',
                                      list_separator='*')
        self.x.read('./test_cfg_kwargs.ini')
        self.x.set_section_separator('%')
        self.assertEqual(self.x.get('sect1', 'key3'), 'val3')

    def test_set_section_separator_fail(self):
        self.x = ExtendedConfigParser(config='',
                                      config_separator='#',
                                      list_separator='*')
        self.x.read('./test_cfg_kwargs.ini')
        self.x.set_section_separator('%')
        self.assertEqual(self.x.get('sect1', 'key3'), 'val3')

    def test_set_list_separator(self):
        self.x = ExtendedConfigParser(config='dev',
                                      config_separator='#',
                                      section_separator='%')
        self.x.read('./test_cfg_kwargs.ini')
        self.x.set_list_separator('*')
        self.assertEqual(self.x.get('sect1', 'key2', isList=True),
                         ['dev2', '2ved', '2vedev2'])

    def test_set_list_separator_wrong(self):
        self.x = ExtendedConfigParser(config='dev',
                                      config_separator='#',
                                      section_separator='%')
        self.x.read('./test_cfg_kwargs.ini')
        self.x.set_list_separator('*')
        self.assertEqual(self.x.get('sect1', 'key_list'), 'damn;dang;nabbit')

    def test_set_inheritance(self):
        self.x.set_inheritance('test')
        self.assertEqual(self.x.inheritance, 'test')

    def test_get_section_name_compact_basic(self):
        self.assertEqual(self.x.get_section_name_compact('sect2'), 'sect2')

    def test_get_section_name_compact_parents(self):
        self.assertEqual(self.x.get_section_name_compact('sect1:sect2:sect3'),
                         'sect1')

    def test_get_first_section(self):
        self.assertEqual(self.x.get_first_section(), 'sect1')


class InheritanceTestCase(unittest.TestCase):

    def setUp(self):
        self.x = ExtendedConfigParser()
        self.x.read('./test_cfg.ini')

    def test_get_section_name(self):
        self.assertEqual(self.x.get_section_name('sect1'), 'sect1:sect2:sect3')

    def test_get_section_name_fail(self):
        self.assertRaises(NoSectionError, self.x.get_section_name, 'sect404')

    def test_get_basic2(self):
        self.assertEqual(self.x.get('sect1', 'key1'), 'val1')

    def test_get_basic_fail2(self):
        self.assertRaises(NoOptionError, self.x.get, 'sect1', 'key412')

    def test_get_sections(self):
        sections = ['sect1:sect2:sect3', 'sect2', 'sect3']
        self.assertEqual(self.x._get_corresponding_sections('sect1'), sections)

    def test_get_sections_return_name(self):
        sections = ['sect3']
        self.assertEqual(self.x._get_corresponding_sections('sect3'), sections)

    def test_get_sections_fail(self):
        self.assertRaises(NoSectionError, lambda:
                          self.x._get_corresponding_sections('sect173'))

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

    def test_get_default_key_dict(self):
        self.assertEqual(self.x['sect1']['key049'], 'DEFAULT')

    def test_get_key_dict_fail(self):
        self.assertRaises(KeyError, lambda: self.x['sect2']['key4'])

    def test_get_sect_dict_fail(self):
        self.assertRaises(KeyError, lambda: self.x['sect42']['key1'])


class InheritModeSelectionTestCase(unittest.TestCase):

    def test_get_sections_method_select_im(self):
        self.x = ExtendedConfigParser(inheritance='im')
        self.x.read('./test_cfg.ini')
        self.assertEqual(
            self.x.get_corresponding_sections('sect4'),
            self.x._get_corresponding_sections_inheritance('sect4'))

    def test_get_sections_method_select_impl(self):
        self.x = ExtendedConfigParser(inheritance='impl')
        self.x.read('./test_cfg.ini')
        self.assertEqual(
            self.x.get_corresponding_sections('sect4'),
            self.x._get_corresponding_sections_inheritance('sect4'))

    def test_get_sections_method_select_implicit(self):
        self.x = ExtendedConfigParser(inheritance='implicit')
        self.x.read('./test_cfg.ini')
        self.assertEqual(
            self.x.get_corresponding_sections('sect4'),
            self.x._get_corresponding_sections_inheritance('sect4'))

    def test_get_sections_method_select_random(self):
        self.x = ExtendedConfigParser(inheritance='Valkyr Prime')
        self.x.read('./test_cfg.ini')
        self.assertEqual(
            self.x.get_corresponding_sections('sect4'),
            self.x._get_corresponding_sections('sect4'))

    def test_get_sections_method_select_default(self):
        self.x = ExtendedConfigParser()
        self.x.read('./test_cfg.ini')
        self.assertEqual(
            self.x.get_corresponding_sections('sect4'),
            self.x._get_corresponding_sections('sect4'))


class InheritModeTestCase(unittest.TestCase):

    def setUp(self):
        self.x = ExtendedConfigParser(inheritance='implicit')
        self.x.read('./test_cfg.ini')

    def test_get_sections_inherit_mode(self):
        sections = ['sect1:sect2:sect3', 'sect2', 'sect3']
        self.assertEqual(
            self.x._get_corresponding_sections_inheritance('sect1'),
            sections)

    def test_get_sections_inherit_mode_return_name(self):
        sections = ['sect3']
        self.assertEqual(
            self.x._get_corresponding_sections_inheritance('sect3'),
            sections)

    def test_get_sections_inherit_mode_fail(self):
        self.assertRaises(
            NoSectionError,
            lambda: self.x._get_corresponding_sections_inheritance('sect173'))

    def test_get_sections_inherit_mode_simple_inherit(self):
        # [sect1:sect2] and [sect2:sect3] => [sect1:sect2:sect3]
        sections = ['sect8:sect5', 'sect5:sect51', 'sect51']
        self.assertEqual(
            self.x._get_corresponding_sections_inheritance('sect8'),
            sections)

    def test_get_sections_inherit_mode_multiple_inherit(self):
        # [sect1:sect2:sect3]  => check [sect2], [sect3] and their parents
        sections = ['sect4:sect5:sect6', 'sect5:sect51',
                    'sect51', 'sect6:sect61', 'sect61']
        self.assertEqual(
            self.x._get_corresponding_sections_inheritance('sect4'),
            sections)

    def test_section_inherit_mode_basic(self):
        res = ['father', 'grandpa', 'key1[dev_plop_toto_stuff]', 'key2',
               'key3', 'key049', 'key049[dev]']
        res.sort()
        test = self.x.options('sect6')
        test.sort()
        self.assertEquals(test, res)

    def test_section_inherit_mode_basic_values(self):
        res = [('father', '6'),
               ('grandpa', '61'),
               ('key1[dev_plop_toto_stuff]', 'dev_plop_toto1_default'),
               ('key2', 'default2'),
               ('key3', 'default3'),
               ('key049', 'DEFAULT'),
               ('key049[dev]', 'DEFAULT_dev')]
        res.sort()
        test = self.x.items('sect6')
        test.sort()
        self.assertEquals(test, res)

    def test_section_inherit_mode_lvl2(self):
        res = ['son', 'father', 'mother', 'grandpa', 'grandma',
               'key1[dev_plop_toto_stuff]', 'key2', 'key3', 'key049',
               'key049[dev]']
        res.sort()
        test = self.x.options('sect8')
        test.sort()
        self.assertEquals(test, res)

    def test_section_inherit_mode_lvl2_values(self):
        res = [('son', '8'),
               ('father', '5'),
               ('mother', '5'),
               ('grandpa', '51'),
               ('grandma', '51'),
               ('key1[dev_plop_toto_stuff]', 'dev_plop_toto1_default'),
               ('key2', 'default2'),
               ('key3', 'default3'),
               ('key049', 'DEFAULT'),
               ('key049[dev]', 'DEFAULT_dev')]
        res.sort()
        test = self.x.items('sect8')
        test.sort()
        self.assertEquals(test, res)

    def test_section_inherit_mode_multiple_inheritance_values_father(self):
        self.assertEquals(self.x.get('sect4', 'father'), '5')

    def test_section_inherit_mode_multiple_inheritance_values_grandpa(self):
        self.assertEquals(self.x.get('sect4', 'grandpa'), '51')


class SpecificationTestCase(unittest.TestCase):

    def setUp(self):
        self.x = ExtendedConfigParser(config='dev')
        self.x.read('./test_cfg.ini')

    def test_get_config_name(self):
        self.assertEqual(self.x.get_config_name(), 'dev')

    def test_specification_basic_unspeced_key(self):
        self.assertEqual(self.x.get('sect2', 'key1'), 'val1_sect2')

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

    def test_get_configs_param(self):
        res = ['dev_plop_toto', 'dev_plop', 'dev']
        self.assertEqual(self.x.get_configs('dev_plop_toto'), res)

    def test_get_configs_plus(self):
        self.x.set_config_name('dev_plop_toto')
        res = ['dev_plop_toto', 'plop_toto', 'toto', 'dev_plop', 'plop', 'dev']
        self.assertEqual(self.x.get_configs_plus(), res)

    def test_get_configs_plus_param(self):
        res = ['dev_plop_toto', 'plop_toto', 'toto', 'dev_plop', 'plop', 'dev']
        self.assertEqual(self.x.get_configs_plus('dev_plop_toto'), res)

    def test_specification_advanced(self):
        self.x.set_config_name('dev_plop_toto')
        self.assertEqual(self.x.get('sect3', 'key3'), 'dev_plop_toto3')

    def test_get_specified_defaults(self):
        self.assertEqual(self.x.get('sect3', 'key049'), 'DEFAULT_dev')

    def test_get_specified_vars(self):
        self.assertEqual(self.x.get('sect1', 'key1', vars={'key1[dev]': 'deez'}
                                    ), 'deez')
