#!/bin/bash

if [ "${TRAVIS_PYTHON_VERSION}" = "2.6" ]; then
  coveralls
fi
