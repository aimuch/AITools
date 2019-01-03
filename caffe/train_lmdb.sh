#!/usr/bin/env sh
set -e

/home/andy/caffe/build/tools/caffe train --solver=/home/andy/caffe/examples/mydata/apa_slot/apa_solver.prototxt $@
