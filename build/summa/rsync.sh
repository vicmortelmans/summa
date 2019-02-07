#!/bin/sh
gsutil -m rsync -x '\.git.*' -r . gs://summa.gelovenleren.net
touch rsync.sh
