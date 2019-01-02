EXAMPLE=/home/andy/caffe/examples/mydata/apa_slot/data
DATA=/home/andy/caffe/examples/mydata/apa_slot/data
TOOLS=/home/andy/caffe/build/tools

rm -rf $DATA/mydata_mean.binaryproto

$TOOLS/compute_image_mean $EXAMPLE/mydata_train_lmdb \
  $DATA/mydata_mean.binaryproto

echo "Done."
