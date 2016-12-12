#!/bin/sh

for f in nginx-*
do
  oldpwd=`pwd`
  cd $f/sbin
  echo Starting $f
  ./nginx -s stop
  cd $oldpwd
done
