 #!/usr/bin/env sh
DATA=data/

echo "Create train.txt..."
rm -rf $DATA/train.txt

find $DATA/train/error -name *.jpg | cut -d '/' -f 4- >> $DATA/train.txt
find $DATA/train/h -name *.jpg | cut -d '/' -f 4- >> $DATA/train.txt
find $DATA/train/h_o -name *.jpg | cut -d '/' -f 4- >> $DATA/train.txt
find $DATA/train/v -name *.jpg | cut -d '/' -f 4- >> $DATA/train.txt
find $DATA/train/v_o -name *.jpg | cut -d '/' -f 4- >> $DATA/train.txt
echo "\n"

echo "Create val.txt..."
rm -rf $DATA/val.txt

find $DATA/val/error -name *.jpg | cut -d '/' -f 4- >> $DATA/val.txt
find $DATA/val/h -name *.jpg | cut -d '/' -f 4- >> $DATA/val.txt
find $DATA/val/h_o -name *.jpg | cut -d '/' -f 4- >> $DATA/val.txt
find $DATA/val/v -name *.jpg | cut -d '/' -f 4- >> $DATA/val.txt
find $DATA/val/v_o -name *.jpg | cut -d '/' -f 4- >> $DATA/val.txt
echo "\n"

echo "Create test.txt..."
rm -rf $DATA/test.txt

#find $DATA/test/error -name *.jpg | cut -d '/' -f 4- >> $DATA/test.txt
#find $DATA/test/h -name *.jpg | cut -d '/' -f 4- >> $DATA/test.txt
#find $DATA/test/h_o -name *.jpg | cut -d '/' -f 4- >> $DATA/test.txt
#find $DATA/test/v -name *.jpg | cut -d '/' -f 4- >> $DATA/test.txt
find $DATA/test/v_o -name *.jpg | cut -d '/' -f 4- >> $DATA/test.txt
echo "\n"

echo "All done!"
