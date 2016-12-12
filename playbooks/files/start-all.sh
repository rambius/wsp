#!/bin/sh

for f in nginx-*
do
  oldpwd=`pwd`
  cd $f/sbin
  echo Starting $f
  ./nginx 
  cd $oldpwd
done
