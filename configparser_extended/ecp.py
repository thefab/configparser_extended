# -*- coding: utf-8 -*-
#
# This file is part of configparser_extended library
# released under the MIT license.
# See the LICENSE file for more information.

import configparser
from configparser import NoOptionError, NoSectionError
from backports.configparser.helpers import OrderedDict
from six import u


# Used in parser getters to indicate the default behaviour when a specific
# option is not found it to raise an exception. Created to enable `None' as
# a valid fallback value.
_UNSET = object()


class ExtendedConfigParser(configparser.ConfigParser):

    # Contains the options read in the DEFAULT section
    default_section = None

    config_name = ''
    config_separator = '_'
    section_separator = ':'
    list_separator = ';'
    father = {}     # Contains the defaults values

    def __init__(self,
                 defaults=None,
                 dict_type=OrderedDict,
                 allow_no_value=False,
                 config='',
                 config_separator='_',
                 section_separator=':',
                 list_separator=';',
                 **kwargs
                 ):

        configparser.ConfigParser.__init__(self,
                                           defaults,
                                           dict_type,
                                           allow_no_value,
                                           **kwargs
                                           )
        # Prevents the get() method from looking into the DEFAULT section
        # before looking into potential parents
        self.default_section = None

        self.config_name = config
        self.config_separator = config_separator
        self.section_separator = section_separator
        self.list_separator = list_separator
        self._proxies[self.
                      default_section] = SectionProxyExtended(self,
                                                              configparser.
                                                              DEFAULTSECT)

        # Prevents the get() method from looking into defaults before
        # looking into potential parents
        self.father = self._defaults.copy()
        self._defaults = {}

    def get(self, section, option, raw=False, vars=None,
            fallback=None, sect_first=True, cfg_plus=False):
        """ Returns the value corresponding to an option in a particular
        section. If vars is provided, it must be a dictionary. The value is
        looked up in vars before being looked up in section. This function
        processes the section name and config name to converte them into valid
        names and then looks for the option value depending on these names.

        You can choose if you want to prioritize the section over the config
        name (sect_first = True) or the config name over the section
        (sect_first = False) if you absolutely want the value corresponding to
        the config.

        ex : Looking for 'option1' in 'section1' with a 'toto_titi' config

            [section1:section2]
            option1[toto]=toto1
            option1=val1

            [section2]
            option1[toto_titi]=toto_titi2

        (sect_first = True) : option1 = toto1
        (sect_first = False) : option1 = toto_titi2
        """

        if(sect_first):
            return self.section_config_loop(section, option, raw, vars,
                                            fallback, cfg_plus)
        else:
            return self.config_section_loop(section, option, raw, vars,
                                            fallback, cfg_plus)

    def section_config_loop(self, section, option, raw=False, vars=None,
                            fallback=None, cfg_plus=False):
        """ Loops on the configs inside a section

        run ex :
             Look for option with and without config name in vars
             Look for option with and without config name in section1:section2
             Look for option with and without config name in section2
             Look for option with and without config name in DEFAULT
             Look for option with and without config name in defaults
        """

        result = None
        sections = self.get_corresponding_sections(section)
        if(not cfg_plus):
            configs = self.get_configs()
        else:
            configs = self.get_configs_plus()

        if(vars is not None):
            for c in configs:
                if (vars.get(option + '[' + c + ']') is not None):
                    return vars.get(option + '[' + c + ']')
            if (vars.get(option) is not None):
                return vars.get(option)

        # Loop on the list of sections
        for s in sections:
            # Loop on the config names
            for c in configs:
                if(self.get_result(s, option, raw, c) is not None):
                    return self.get_result(s, option, raw, c)

            # Look for the option without any specific config name
            if(self.get_result(s, option, raw) is not None):
                return self.get_result(s, option, raw)

        # Look for the option in the DEFAULT section, in defaults and, finally,
        # in fallback
        for c in configs:
            if(result is None):
                if(option in self.default_section):
                    result = self.default_section.get(option + '[' + c + ']')
                    break

        for c in configs:
            if(result is None):
                if(option in self.father):
                    result = self.father.get(option + '[' + c + ']')
                    break

        if(result is None):
            if(option in self.default_section):
                result = self.default_section.get(option)

        if(result is None):
            if(option in self.father):
                result = self.father.get(option)

        if(result is None):
            result = fallback

        if(result is None):
            # If nothing has been found, raise an exception
            raise NoOptionError(option, section)

        result = self.convert_value_list(result)
        return result

    def config_section_loop(self, section, option, raw=False, vars=None,
                            fallback=None, cfg_plus=False):
        """ Loops on the sections per config name

        run ex :
             Look for option[cfg1] in every section
             Look for option[cfg2] in every section
             Look for option in every section
        """

        result = None
        sections = self.get_corresponding_sections(section)
        if(not cfg_plus):
            configs = self.get_configs()
        else:
            configs = self.get_configs_plus()

        if(self.config_name != '' and self.config_name is not None):
            # Loop on the config names
            for c in configs:

                # Search into vars
                if(vars is not None):
                    if (vars.get(option + '[' + c + ']') is not None):
                        return vars.get(option + '[' + c + ']')

                # Loop on the list of sections
                for s in sections:
                    if(self.get_result(s, option, raw, c) is not None):
                        return self.get_result(s, option, raw, c)

                # Look for the option in the DEFAULT section, in defaults
                if(result is None):
                    if(option + '[' + c + ']' in self.default_section):
                        result = self.default_section.get(option + '[' + c +
                                                          ']')
                        break

                if(result is None):
                    if(option + '[' + c + ']' in self.father):
                        result = self.father.get(option + '[' + c + ']')
                        break

        if(result is None):
            # Look for the option without any specific config name
            if(vars is not None):
                if (vars.get(option) is not None):
                    return vars.get(option)

            # Loop on the list of sections
            for s in sections:
                if(self.get_result(s, option, raw) is not None):
                    return self.get_result(s, option, raw)

            # Look for the option in the DEFAULT section, in defaults and,
            # finally, in fallback
            if(result is None):
                if(option in self.default_section):
                    result = self.default_section.get(option)

            if(result is None):
                if(option in self.father):
                    result = self.father.get(option)

        if(result is None):
            result = fallback

        if(result is None):
            # If nothing has been found, raise an exception
            raise NoOptionError(option, section)

        result = self.convert_value_list(result)
        return result

    def get_result(self, s, option, raw=False, c=''):
        if(c == '' or c is None):
            try:
                result = self.find_option(s, option, raw)
                if(result is not None):
                    result = self.convert_value_list(result)
                    return result
            except NoOptionError:
                pass
        else:
            try:
                result = self.find_option(s, option, raw, c)
                if(result is not None):
                    result = self.convert_value_list(result)
                    return result
            except NoOptionError:
                pass

    def find_option(self, section, option, raw=False, config=''):
        """ Returns the result of a basic get() where section and config have
        already been processed/converted into valid names. It functions just as
        the original get() does while being able to return a result associated
        with a config name. """

        try:
            # If no config name is precised, look for the option without
            # "[config]"
            if(config == ''):
                return super(ExtendedConfigParser, self).get(section, option,
                                                             raw=raw)

            # Look for the option with the config name specified between
            # a pair of brackets (ex : key1[config1]=val1 )
            # NoSectionError raised by get_no_def()
            else:
                return super(ExtendedConfigParser, self).get(section, option
                                                             + '[' + config +
                                                             ']', raw=raw)

        except NoOptionError:
            pass

    def get_corresponding_sections(self, section):
        """ Look for the actual name of the section if it inherits from other
        sections and stores the section name itself as well as its parents'.
        """

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
        return sections

    def get_section_name(self, section):
        """ Returns the actual name of the section inside the read source if
        it inherits from some other source. """

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

    def get_section_name_compact(self, section):
        """ Returns the name of the section without its parents. """

        if(self.section_separator in section):
            sect = section[:section.find(self.section_separator)]
        else:
            sect = section
        return sect

    def get_first_section(self):
        """ Returns the compact name of the first section """
        for s in self._sections:
            s = self.get_section_name_compact(s)
            return s

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
        """ Stores and returns the config name itself
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
        """ Converts a value into a List if it contains self.list_separator or
        returns the value if it doesn't. """

        if(self.list_separator in val):
            list_val = val.split(self.list_separator)
            return list_val
        else:
            return val

    def getint(self, section, option, raw=False, vars=None,
               fallback=None):
        """ Returns the value of an option as an integer. """

        res = self.get(section, option, raw, vars, fallback)
        if(self.is_list(res)):
            res = [int(i) for i in res]
        else:
            res = int(res)
        return res

    def getfloat(self, section, option, raw=False, vars=None,
                 fallback=None):
        """ Returns the value of an option as an double. """

        res = self.get(section, option, raw, vars, fallback)
        if(self.is_list(res)):
            res = [float(i) for i in res]
        else:
            res = float(res)
        return res

    def getboolean(self, section, option, raw=False, vars=None,
                   fallback=None):
        """ Returns the value of an option as a boolean. """

        res = self.get(section, option, raw, vars, fallback)
        if(self.is_list(res)):
            res = [self.str_to_bool(i) for i in res]
        else:
            res = self.str_to_bool(res)
        return res

    def str_to_bool(self, string):
        """ Returns True if the lowered string is "true", "yes", "on" or "1".
        Returns False if the lowered string is "false", "no", "off" or "0".
        Raises ValueError otherwise """

        string = string.lower()
        if(string == 'true' or string == 'yes' or string == 'on' or
           string == '1'):
            return True
        elif(string == 'false' or string == 'no' or string == 'off' or
             string == '0'):
            return False
        else:
            raise ValueError(string)

    def is_list(self, res):
        if isinstance(res, list):
            return True
        else:
            return False

    def get_config_name(self):
        return self.config_name

    def set_config_name(self, config):
        self.config_name = config

    def read(self, filenames, encoding=None):
        """Read and parse a filename or a list of filenames.

        Files that cannot be opened are silently ignored; this is
        designed so that you can specify a list of potential
        configuration file locations (e.g. current directory, user's
        home directory, systemwide directory), and all existing
        configuration files in the list will be read.  A single
        filename may also be given.

        Return list of successfully read files.
        """

        filenames = u(filenames)
        super(ExtendedConfigParser, self).read(filenames, encoding)
        self.move_defaults()

    def read_file(self, f, source=None):
        """Like read() but the argument must be a file-like object.

        The `f' argument must be iterable, returning one line at a time.
        Optional second argument is the `source' specifying the name of the
        file being read. If not given, it is taken from f.name. If `f' has no
        `name' attribute, `<???>' is used.
        """

        super(ExtendedConfigParser, self).read_file(f, source)
        self.move_defaults()

    def move_defaults(self):
        """ Transfers the content from the DEFAULT section to
        self.default_section to prevent get() from returning DEFAULT
        option values instead of parent option values and "converts"
        SectionProxies to SectionProxiesExtended. """

        try:
            self.default_section = self._sections['DEFAULT'].copy()
            del self._sections['DEFAULT']
        except KeyError:
            pass
        # "Convert" SectionProxies to SectionProxiesExtended
        for s in self._sections:
            self._proxies[s] = SectionProxyExtended(self, s)

    def has_option(self, section, option, config='', cfg_ind=False,
                   strict=False):
        """ Returns True if the option has been found, returns False
        otherwise. See the sub-methods' documentation for more details. """
        if(strict):
            if(cfg_ind):
                return self._has_option_strict_config_ind(section, option)
            else:
                return self._has_option_strict(section, option, config)
        else:
            if(cfg_ind):
                return self._has_option_config_ind(section, option)
            else:
                return self._has_option(section, option, config)

    def _has_option(self, section, option, config=''):
        """ Returns True if the option is explicitly defined in the section or
        inherited from another section for the current config name (or for the
        config name precised in the parameters) and returns False otherwise."""

        if(self.has_section(section)):
            sections = self.get_corresponding_sections(section)
            if(config != '' and config is not None):
                configs = self.get_configs(config)
            else:
                configs = self.get_configs()
            for s in sections:
                for c in configs:
                    res = super(ExtendedConfigParser, self).has_option(s,
                                                                       option +
                                                                       '[' + c
                                                                       + ']')
                    if(res):
                        return True

                res = super(ExtendedConfigParser, self).has_option(s, option)
                if(res):
                    return True
            return False

    def _has_option_strict(self, section, option, config=''):
        """ Returns True only if the option is explicitly defined in the
        section for the current config name (or for the config name precised in
        the parameters) and returns False otherwise. """

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

    def _has_option_config_ind(self, section, option):
        """ Returns True if the option is explicitly defined in the section or
        inherited from another section, having a config name specified or not,
        and returns False otherwise. """

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

    def _has_option_strict_config_ind(self, section, option):
        """ Returns True only if the option is explicitly defined in the
        section, having a config name specified or not, and returns False
        otherwise. """

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

    def has_section(self, section, strict=False):
        """ Returns True if the section name entered is found in the file. If
        strict is True, it will look for the exact given section name. If
        strict is False, it will look for the given name with eventual
        inheritance signs. See the sub-methods' documentation for more details.
        """
        if(strict):
            return self._has_section_strict(section)
        else:
            return self._has_section(section)

    def _has_section(self, section):
        """ Checks if there is a section associated with the section name
        entered.
        ex : self.has_section('sect1') will return True if 'sect1:sect2' exists
        """

        try:
            s = self.get_section_name(section)
            if(s is not None):
                return True
        except NoSectionError:
            return False

    def _has_section_strict(self, section):
        """ Checks if the section name entered exists. """

        return section in self._sections

    def add_section(self, section):
        section = u(section)
        super(ExtendedConfigParser, self).add_section(section)
        self._proxies[section] = SectionProxyExtended(self, section)

    def __getitem__(self, key):
        try:
            s = self.get_section_name(key)
        except NoSectionError:
            raise KeyError(key)
        return super(ExtendedConfigParser, self).__getitem__(s)

    def defaults(self):
        return self.father

    def items(self, section=_UNSET, raw=False, vars=None,
              strict=False, defaults=False):
        """ Returns a list of (name, value) tuples for each option in a section
        excluding its parents. If defaults is True though, the DEFAULT section
        will be included. When section is not given, return a list of
        section_name, section_proxy pairs, including DEFAULTSECT.

        All % interpolations are expanded in the return values, based on the
        defaults passed into the constructor, unless the optional argument
        `raw' is true.  Additional substitutions may be provided using the
        `vars' argument, which must be a dictionary whose contents overrides
        any pre-existing defaults.

        The DEFAULT section is special.
        """

        if(strict):
            return self._items_strict(section, raw, vars, defaults)
        else:
            return self._items(section, raw, vars)

    def _items(self, section=_UNSET, raw=False, vars=None):
        """ Returns a list of (name, value) tuples for each option in a section
        and all of its parents. """

        res = []
        if(section is None or section is _UNSET):
            res = self._items_empty()
        else:
            sections = self.get_corresponding_sections(section)
            for s in sections:
                res += (super(ExtendedConfigParser, self).items(s, raw,
                                                                vars))
            defaults = (list(self.default_section.items()) +
                        list(self.father.items()))
            res += (defaults)
        return res

    def _items_strict(self, section=_UNSET, raw=False, vars=None,
                      defaults=False):
        """ Returns a list of (name, value) tuples for each option in a section
        excluding its parents. If defaults is True though, the DEFAULT section
        will be included. """

        if(defaults):
            self._defaults.update(self.father)
            self._defaults.update(self.default_section)
        if(section is None or section is _UNSET):
            res = self._items_empty()
        else:
            sect = self.get_section_name(section)
            res = super(ExtendedConfigParser, self).items(sect, raw, vars)
        self._defaults = {}
        return res

    def _items_empty(self):
        """ Returns a list of section_name, section_proxy pairs, including
        DEFAULTSECT. """

        return [(sect, self[sect]) for sect in self._sections]

    def options(self, section, strict=False, defaults=False):
        """ Returns a list of option names for the given section and its
        parents if strict is False, or, if strict is True, returns a list of
        option names for the given section only. If defaults and strict are
        True, DEFAULT options will be included. """

        if(strict):
            return self._options_strict(section, defaults)
        else:
            return self._options(section)

    def _options(self, section):
        """ Returns a list of option names for the given section and its
        parents. """

        res = []
        sections = self.get_corresponding_sections(section)
        for s in sections:
            res += super(ExtendedConfigParser, self).options(s)
        if(self.default_section is not None):
            res += list(self.default_section.keys())
        if(self.father is not None):
            res += list(self.father.keys())
        return res

    def _options_strict(self, section, defaults=False):
        """ Returns a list of option names for the given section only. If
        defaults is True, DEFAULT options will be included. """

        sect = self.get_section_name(section)
        res = super(ExtendedConfigParser, self).options(sect)
        if(defaults):
            if(self.default_section is not None):
                res += list(self.default_section.keys())
            if(self.father is not None):
                res += list(self.father.keys())
        return res

    def set_config_separator(self, separator):
        self.config_separator = separator

    def set_section_separator(self, separator):
        self.section_separator = separator

    def set_list_separator(self, separator):
        self.list_separator = separator


class SectionProxyExtended(configparser.SectionProxy):
    """ A proxy for a single section from a parser. Designed to support
    inheritance. """

    def __init__(self, parser, name):
        self._parser = parser
        self._name = name

    def __getitem__(self, key):
        try:
            return self._parser.get(self._name, key)
        except NoOptionError:
            raise KeyError(key)
