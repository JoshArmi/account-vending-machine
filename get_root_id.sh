#!/bin/bash

set -e

ID=$(aws organizations list-roots | jq '.Roots[0].Id' | sed 's/"//g')

jq -n --arg root $ID '{"id":$root}'
