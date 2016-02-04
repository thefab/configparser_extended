# configparser_extended

## Status (master branch)

[![Build Status](https://travis-ci.org/thefab/configparser_extended.png)](https://travis-ci.org/thefab/configparser_extended)
[![Coverage Status](https://coveralls.io/repos/thefab/configparser_extended/badge.png)](https://coveralls.io/r/thefab/configparser_extended)
[![Code Health](https://landscape.io/github/thefab/configparser_extended/master/landscape.png)](https://landscape.io/github/thefab/configparser_extended/master)
[![Requirements Status](https://requires.io/github/thefab/configparser_extended/requirements.png?branch=master)](https://requires.io/github/thefab/configparser_extended/requirements/?branch=master)

**WARNING : it is strongly advised to read the original ConfigParser documentation if you're a beginner**

## What is it ?

A python configparser extension which implements a few addons like:

- distinct option values depending on the "configuration" of an application (DEV, TESTS, PRODUCTION...)
- section inheritance

This extension is supposed to implement these new functionnalities without changing the base behavior of the original ConfigParser. You should be able to switch from the original ConfigParser to ConfigParserExtended without changing your code too much.

*As this project is open source, feel free to add new functionnalities that could help the community and report any bug that you encounter.*

## Option specification : values depending on the configuration's name

### Basics

This functionnality, as the name suggests it, allows you to **define option values for a specific configuration name** : 

    [section1]
    option1=foo
    option1[server]=bar

In this case, the value of `option1` will be `foo` for any configuration name except for the `server` configuration : the value of `option1` will be `bar` for the `server` configuration only.

The configuration name can be set in 2 ways : either in the constructor with `config_name=` or via the `set_config_name()` method.

### Inheritance

Inheritance is also available for configuration names as well. This allows you to get specific values without having to define an option exclusively for that :

    [section1]
    option1=val1
    option1[server]=server1
    option1[server_eu]=server_eu1
    option1[server_eu_fr]=server_eu_fr1
    option2=val2
    option2[server]=server2
    option2[server_eu]=server_eu2
    option3=val3
    option3[server]=server3

From this config file, we can obtain different values depending on the config name :

- for the 'server' configuration, the values for the 3 options will be :

    [section1]
    option1[server]=server1
    option2[server]=server2
    option3[server]=server3

- for the 'server_usa' configuration, the values for the 3 options will be :

    [section1]
    option1[server]=server1
    option2[server]=server2
    option3[server]=server3

- for the 'server_eu_gb' configuration, the values for the 3 options will be :

    [section1]
    option1[server_eu]=server_eu1
    option2[server_eu]=server_eu2
    option3[server]=server3

- for the `server_eu_fr` configuration, the values for the 3 options will be :

    [section1]
    option1[server_eu_fr]=server_eu_fr1
    option2[server_eu]=server_eu2
    option3[server]=server3

Basically, with a `foo_bar_baz` configuration name, ConfigParserExtended will look for :

1. `option[foo_bar_baz]`
2. `option[foo_bar]`
3. `option[foo]`
4. `option`

There is also another "version" of this function which will look for :

1. `option[foo_bar_baz]`
2. `option[bar_baz]`
3. `option[baz]`
4. `option[foo_bar]`
5. `option[bar]`
6. `option[foo]`
7. `option`

You can use this version via the `get()` method by setting the `sect_first` parameter to false.

### Syntax

**Syntax : `option[grandparent_parent_child]=value`**

Note that the separator '_' is customizable via the constructor.

## Section inheritance

### Basics

This functionnality allows you to **define "fallback sections" for any particular section** :

    [section1:section2:section3]
    option1=val1

    [section2]
    option2=val2

    [section3]
    option2=val2_sect3
    option3=val3

    [DEFAULT]
    option1=default1
    option2=default2
    option3=default3
    option4=default4

In this case, `section2` and `section3` serve as fallback sections, prioritized over the `DEFAULT` section, for `section1`. The list of items in `section1` will be :

    [section1]
    option1=val1
    option2=val2
    option3=val3
    option4=default4

As you can see, it is possible to have multiple fallback sections but **they are prioritized from left to right** (see `option2`). You can consider that every section "inherits" from the `DEFAULT` section. **Warning, writing `section1:section2:section3` doesn't imply that `section2:section3`!!!**

### Usage with option specification

In ConfigParserExtended, by default, the search using configuration names is done on a section scale, not on the whole file. Thus, if an option has been found in a child section, the option will be returned and the parent section will not be searched. Example with a `dev` configuration : 

    [section1:section2]
    option1=val1

    [section2]
    option1[dev]=dev1

The value of `option1` for `section1` will be `val1` here. However, if you want to get `dev1` instead of `val1` with the same parameters, you can set the `sect_first` parameter to `False` in the `get()` method.

### Syntax

**Syntax : `[grandparent:parent:child]**

Note that the separator ':' is customizable via the constructor

## Miscellaneous

Some methods have been adapted to this new functionnalities by adding options to take in account option specification and inheritance, or not. Keep in mind that these methods have the exact same roles as in the original ConfigParser.

### `has_option()`

This function has now 3 additional optional parameters :

- `config` : enter a configuration name to use `has_option` for this specific name

- `cfg_ind` : if True, the function will return True if the option has been found, regardless of the specified configuration name. If False (default), the function will return True only if the option has been found either without specification, or specified with the current configuration name (or `config` if set).

- `strict` : if True, the function will only search the given section, but neither the parent section(s) nor the `DEFAULT` section will be searched. If False (default), the given section will be searched as well as its parent(s) and the `DEFAULT` section.

A little example with a `aye` config name using `has_option('section1',option1):

    [section1:section2]
    option1[nope]=nope1

    [section2]
    option1=val1

- `strict=False` ; `cfg_ind=False`  =>  return `True`

- `strict=True` ; `cfg_ind=False`  =>  return `False`

- `strict=True` ; `cfg_ind=False` ; `config=nope`  =>  return `True`

- `strict=False` ; `cfg_ind=True`  =>  return `True`

- `strict=True` ; `cfg_ind=True`  =>  return `True`

## has_section

This function has got an additional boolean parameter, `strict`, which will decide if the function looks for the exact given section name (`strict=True`) or if the function looks for eventual inheritance signs(`strict=True`, default). Here's a small example using `has_section('section1')` :

    [section1:section2]
    random=stuff

    [section2]
    really=random

- `strict=False`  =>  return `True`

- `strict=True`  =>  return `False` because `section1` != `section1:section2` here

### `items()`

This function now has the same `strict` optional parameter as `has_option()` which plays the exact same role : if True, the function will return a list of option-value tuples from the section only, and, if False (default), will return a list of option-value tuples from the section, its parents and the `DEFAULT` section.

### `options()`

This function now has the same `strict` optional parameter as `has_option()` which plays the exact same role : if True, the function will return a list of options from the section only, and, if False (default), will return a list of options from the section, its parents and the `DEFAULT` section.

## Special thanks

- The configparser dev team 
- The six dev team
- The Python dev team
- thefab
- Météo France


