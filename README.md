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
- file inclusion

This extension is supposed to implement these new functionnalities without changing the base behavior of the original ConfigParser. You should be able to switch from the original ConfigParser to ConfigParserExtended without changing too much your code.

As this project is open source, feel free to add new functionnalities that could help the community.

## Option specification : values depending on the configuration's name

### Basics

This functionnality, as the name suggests it, allows you to **define option values for a specific configuration name** : 

    [section1]
    option1=foo
    option1[server]=bar

In this case, the value of `option1` will be `foo` for any configuration name except for the `server` configuration : the value of `option1` will be `bar` for the `server` configuration only.

The configuration name can be set in 2 ways : either in the constructor with `config_name=` or via the `set_config_name()`.

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

Basically, ConfigParserExtended will look for :

1. `option[foo_bar_baz]`
2. `option[foo_bar]`
3. `option[foo]`
4. `option`

There is alson another "version of this function which will look for :

1. `option[foo_bar_baz]`
2. `option[bar_baz]`
3. `option[baz]`
4. `option[foo_bar]`
5. `option[bar]`
6. `option[foo]`
7. `option`

For now, this function is only available by changing a line of code in the get() method.

### Syntax

**Syntax : `option[grandparent_parent_child]=value`**

Note that the separator '_' is customizable via the constructor

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

In this case, `section2` and `section3` serve as fallback sections prioritized over the `DEFAULT` section for `section1`. The list of items in `section1` will be :

    [section1]
    option1=val1
    option2=val2
    option3=val3
    option4=default4

As you can see, it is possible to have multiple fallback sections but **they are prioritized from left to right** (see `option2`). **Warning, writing `section1:section2:section3` doesn't imply that `section2:section3`!!!**

### Usage with option specification

In ConfigParserExtended, the research using configuration names is done inside a section and not inside a file, thus, if an option has been found in a child section, the option will be returned and the parent section will not be searched. Example with a `dev` configuration : 

    [section1:section2]
    option1=val1

    [section2]
    option1[dev]=dev1

The value of `option1` for `section1` will be `val1` here. However, if you want to get `dev1` instead of `val1` with the same parameters, you can set the `sect_first` parameter to `False` in the `get()` method (**NOT WORKING YET***).

### Syntax

**Syntax : `[grandparent:parent:child]**

Note that the separator ':' is customizable via the constructor


