# -*- coding: utf-8 -*-
#
# This file is part of configparser_extended library
# released under the MIT license.
# See the LICENSE file for more information.

import configparser
from configparser import NoOptionError, NoSectionError
from collections import OrderedDict


class ExtendedConfigParser(configparser.ConfigParser):

    # Contains the options read in the DEFAULT section
    default_section = None

    config_name = ''
    config_separator = '_'
    section_separator = ':'
    father = {}     # Contains the defaults values

    def __init__(self,
                 defaults=None,
                 dict_type=OrderedDict,
                 allow_no_value=False,
                 delimiters=('=', ':'),
                 comment_prefixes=('#', ';'),
                 inline_comment_prefixes=(';',),
                 strict=True,
                 empty_lines_in_values=True,
                 default_section=configparser.DEFAULTSECT,
                 interpolation=configparser.BasicInterpolation,
                 converters=None,
                 config='',
                 config_separator='_',
                 section_separator=':'
                 ):

        configparser.ConfigParser.__init__(self,
                                           defaults,
                                           dict_type,
                                           allow_no_value,
                                           # delimiters,
                                           # comment_prefixes,
                                           # inline_comment_prefixes,
                                           # empty_lines_in_values,
                                           # default_section,
                                           # interpolation,
                                           # converters
                                           )
        # Prevents the get() method from looking into the DEFAULT section
        # before looking into potential parents
        self.default_section = None

        self.config_name = config
        self.config_separator = config_separator
        self.section_separator = section_separator
        self._proxies[default_section] = SectionProxyExtended(self,
                                                              configparser.
                                                              DEFAULTSECT)

        # Prevents the get() method from looking into defaults before
        # looking into potential parents
        self.father = self._defaults.copy()
        self._defaults = {}

    def get(self, section, option, raw=False, vars=None,
            fallback=None):
        """ Returns the value corresponding to an option in a particular
        section. If vars is provided, it must be a dictionary. The value is
        looked up in vars before being looked up in section. This function
        processes the section name and config name to converte them into valid
        names and then looks for the option value depending on these names. """

        result = None
        sections = self.get_corresponding_sections(section)
        configs = self.get_configs()

        if(vars is not None):
            if (vars.get(option) is not None):
                return vars.get(option)

        # Loop on the list of sections
        for s in sections:

            try:
                # Loop on the config names
                for c in configs:
                    try:
                        result = self.find_option(s, option, raw, c)
                        if(result is not None):
                            result = self.convert_value_list(result)
                            print '*** sect : ' + str(s) + ' ; cfg : ' + \
                                  str(c) + ' ; res : ' + str(result) + ' ***'
                            return result
                    except NoOptionError:
                        pass

                # Look for the option without any specific config name
                try:
                    result = self.find_option(s, option, raw)
                    if(result is not None):
                        result = self.convert_value_list(result)
                        return result
                except NoOptionError:
                    pass

            except NoSectionError:
                pass

        if(result is None):
            if(option in self.default_section):
                print 'Die Fult'
                result = self.default_section.get(option)

        if(result is None):
            if(option in self.father):
                print 'You just got Father\'ed'
                result = self.father.get(option)

        if(result is None):
            print 'Fall back!'
            result = fallback

        if(result is None):
            # If nothing has been found, raise an exception
            raise NoOptionError(option, section)

        result = self.convert_value_list(result)
        return result

    def find_option(self, section, option, raw=False, config=''):
        """ Returns the result of a basic get() where section and config have
        already been processed/converted into valid names. It functions just as
        get() does while being able to return a result associated with a config
        name. """
        try:
            # If no config name is precised, look for the option without
            # "[config]"
            if(config == ''):
                print '***** section : ' + section + '; option : ' + option + \
                      ' *****'
                return super(ExtendedConfigParser, self).get(section, option,
                                                             raw=raw)

            # Look for the option with the config name specified between
            # a pair of brackets (ex : key1[config1]=val1 )
            # NoSectionError raised by get_no_def()
            else:
                print '***** section : ' + section + '; option : ' + option + \
                      '[' + config + '] *****'
                return super(ExtendedConfigParser, self).get(section, option
                                                             + '[' + config +
                                                             ']', raw=raw)

        except NoOptionError:
            pass

    def get_corresponding_sections(self, section):
        """ Look for the actual name of the section if it inherits from other
        sections and stores the section name itself as well as its parents
        present in the read source """
        # Find the corresponding section if it inherits from another section
        sect = self.get_section_name(section)

        # Store all of the valid section names corresponding to the initial
        # section (the section itself and its parents if they actually exist)
        sections = []
        section_name_edited = self.get_section_name(section)
        while(self.section_separator in section_name_edited):
            if section_name_edited in self._sections:
                sections.append(section_name_edited)
            section_name_edited = section_name_edited[section_name_edited.find(
                                                      self.section_separator)
                                                      + 1:]

        section_splitted = sect.split(self.section_separator)
        for s in section_splitted:
            if s in self._sections:
                sections.append(s)

        # If the list of corresponding sections is empty, raise an exception
        if(not sections):
            raise NoSectionError(section)
        return sections

    def get_section_name(self, section):
        """ Returns the actual name of the section inside the read source if
        it inherits from some other source """
        if(section in self._sections):
            return section

        for sect in self._sections:
            if(self.section_separator in sect):
                subsect = sect[:sect.find(self.section_separator)]
            else:
                subsect = sect

            if (subsect == section):
                return sect
        raise NoSectionError(section)

    def get_configs(self, config=''):
        """ Returns a config name and its direct parents.

        ex : foo_bar_baz, foo_bar, foo"""
        configs = []
        if(config != '' and config is not None):
            config_name_edited = config
        else:
            config_name_edited = self.config_name
        # foo_bar_baz and foo_bar here
        while(self.config_separator in config_name_edited):
            configs.append(config_name_edited)
            config_name_edited = config_name_edited[:config_name_edited.rfind(
                                                    self.config_separator)]
        configs.append(config_name_edited)
        return configs

    def get_configs_plus(self, config=''):
        """ Basically, this function stores and returns the config name itself
        with all its possible names and all of its possible parents.

        ex : foo_bar_baz, bar_baz, baz, foo_bar, bar, foo

        run ex :
            work on foo_bar_baz:
                store foo_bar_baz, bar_baz, baz
            work on foo_bar:
                store foo_bar, bar
            work on foo:
                store foo
        """

        configs = []
        if(config != '' and config is not None):
            config_name_edited = config
        else:
            config_name_edited = self.config_name
        while(self.config_separator in config_name_edited):
            configs.append(config_name_edited)
            cfg = config_name_edited
            while(self.config_separator in cfg):

                # Remove the first name before the separator
                # (default : '_')
                cfg = cfg[cfg.find(self.config_separator)+1:]
                configs.append(cfg)

            # Work on the config's parent (baz -> bar)
            config_name_edited = config_name_edited[:config_name_edited.
                                                    rfind(self.
                                                          config_separator)]
        configs.append(config_name_edited)
        return configs

    def convert_value_list(self, val):
        """ Converts a value into a List if it contains ';' or returns the
        value if it doesn't """
        if(';' in val):
            list_val = val.split(';')
            return list_val
        else:
            return val

    def getint(self, section, option, raw=False, vars=None,
               fallback=None):
        """ Returns the value of an option as an integer """
        res = self.get(section, option, raw, vars, fallback)
        if(self.is_list(res)):
            res = [int(i) for i in res]
        else:
            res = int(res)
        return res

    def getfloat(self, section, option, raw=False, vars=None,
                 fallback=None):
        """ Returns the value of an option as an double """
        res = self.get(section, option, raw, vars, fallback)
        if(self.is_list(res)):
            res = [float(i) for i in res]
        else:
            res = float(res)
        return res

    def getboolean(self, section, option, raw=False, vars=None,
                   fallback=None):
        """ Returns the value of an option as a boolean """
        res = self.get(section, option, raw, vars, fallback)
        if(self.is_list(res)):
            res = [self.str_to_bool(i) for i in res]
        else:
            res = self.str_to_bool(res)
        return res

    def str_to_bool(self, string):
        """ Returns True if the lowered string is "true", "yes", "on" or "1".
        Returns False otherwise"""
        res = False
        string = string.lower()
        if(string == 'true' or string == 'yes' or string == 'on' or
           string == '1'):
            res = True
        return res

    def is_list(self, res):
        if isinstance(res, list):
            return True
        else:
            return False

    def get_config_name(self):
        return self.config_name

    def set_config_name(self, config):
        self.config_name = config

    def read(self, filenames):
        filenames = unicode(filenames, 'utf-8')
        configparser.ConfigParser.read(self, filenames)
        try:
            # Transfer the content from the DEFAULT section to
            # self.default_section to prevent get() from returning DEFAULT
            # option values instead of parent option values
            self.default_section = self._sections['DEFAULT'].copy()
            del self._sections['DEFAULT']
        except KeyError:
            pass
        # "Convert" SectionProxies to SectionProxiesExtended
        for s in self._sections:
            self._proxies[s] = SectionProxyExtended(self, s)

    def has_option(self, section, option, config=''):
        """ Returns True if the option is explicitly defined in the section or
        inherited from another section for the current config name (or for the
        config name precised in the parameters) and returns False otherwise"""

        if(self.has_section(section)):
            sections = self.get_corresponding_sections(section)
            if(config != '' and config is not None):
                configs = self.get_configs(config)
            else:
                configs = self.get_configs()
            for s in sections:
                for c in configs:
                    print "[" + s + " ; " + c + "]"
                    res = super(ExtendedConfigParser, self).has_option(s,
                                                                       option +
                                                                       '[' + c
                                                                       + ']')
                    if(res):
                        return True

                print "[" + s + " ; ]"
                res = super(ExtendedConfigParser, self).has_option(s,
                                                                   option)
                if(res):
                    return True
            return False

    def has_option_strict(self, section, option, config=''):
        """ Returns True only if the option is explicitly defined in the
        section for the current config name (or for the config name precised in
        the parameters) and returns Flase otherwise"""

        sect = self.get_section_name(section)
        if(self.has_section(section)):
            if(config != '' and config is not None):
                configs = self.get_configs(config)
            else:
                configs = self.get_configs()
            for c in configs:
                res = super(ExtendedConfigParser, self).has_option(sect, option
                                                                   + '[' + c +
                                                                   ']')
                if(res):
                    return True
            res = super(ExtendedConfigParser, self).has_option(sect,
                                                               option)
            if(res):
                    return True
            return False

    def has_option_config_ind(self, section, option, config=''):
        """ Returns True if the option is explicitly defined in the section or
        inherited from another section, independantly of the config name, and
        returns False otherwise"""

        if(self.has_section(section)):
            sections = self.get_corresponding_sections(section)
            for s in sections:
                for o in self._sections[s]:
                    if('[' in o):
                        opt = o[:o.find('[')]
                    else:
                        opt = o
                    if(option == opt):
                        return True

            return False

    def has_option_strict_config_ind(self, section, option, config=''):
        """ Returns True only if the option is explicitly defined in the
        section, independantly of the config name, and returns False otherwise
        """

        if(self.has_section(section)):
            sect = self.get_section_name(section)
            for o in self._sections[sect]:
                if('[' in o):
                    opt = o[:o.find('[')]
                else:
                    opt = o
                if(option == opt):
                    return True

            return False

    def has_section(self, section):
        """ Checks if there is a section associated with the section name
        entered
        ex : self.has_section('sect1') will return True if 'sect1:sect2' exists
        """

        try:
            s = self.get_section_name(section)
            if(s is not None):
                return True
        except NoSectionError:
            return False

    def has_section_strict(self, section):
        """ Checks if the section name entered exists """

        super(ExtendedConfigParser, self).has_section(section)

    def add_section(self, section):
        super(ExtendedConfigParser, self).add_section(self, section)
        self._proxies[section] = SectionProxyExtended(self, section)

    def __getitem__(self, key):
        try:
            s = self.get_section_name(key)
        except NoSectionError:
            raise KeyError(key)
        return super(ExtendedConfigParser, self).__getitem__(s)

    def defaults(self):
        return self.father


class SectionProxyExtended(configparser.SectionProxy):
    """A proxy for a single section from a parser."""

    def __init__(self, parser, name):
        self._parser = parser
        self._name = name

    def __getitem__(self, key):
        try:
            return super(SectionProxyExtended, self).__getitem__(key)
        except NoOptionError:
            raise KeyError(key)
