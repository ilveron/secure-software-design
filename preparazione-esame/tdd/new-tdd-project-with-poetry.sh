#!/bin/bash

if [ -z "$1" ]; then
  name="exercise"
else
  name=$1
fi

poetry new "$name"
cd "$name"
package_name=$(echo "$name" | sed -e 's/-/_/g')
touch $package_name/exercise.py
touch tests/test_exercise.py

poetry add pytest valid8 typeguard dataclass-type-validator coverage

