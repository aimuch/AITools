#!/bin/bash
# file tree:
# data
# |--train               |--val                   |--test
# |--|--class1           |--|--class1             |--|--class1        
# |--|--|--folder1       |--|--|--folder1         |--|--|--folder1


DATA=/home/andy/caffe/examples/mydata/conerClassifier/data

TRAIN_PATH=$DATA/train
VAL_PATH=$DATA/val
TEST_PATH=$DATA/test

# classes
CLASSES=('L' 'T')


## Train
echo "Create train.txt..."
rm -rf $DATA/train.txt
LABEL=0
for c in ${CLASSES[@]}
do
    is_folder=1
    for i in $TRAIN_PATH/$c
    do
        # Process folders
        if test -d $i
        then
            find $i -name *.jpg | cut -d '/' -f 10- | sed "s/$/ ${LABEL}/" >> $DATA/train.txt
        fi

        # Process files
        if test -f $i
        then
            is_folder=0
            break
        fi
    done

    if [ $is_folder -eq 0 ]
    then
        find $TRAIN_PATH/$c -name *.jpg | cut -d '/' -f 10- | sed "s/$/ ${LABEL}/" >> $DATA/train.txt
    fi
    ((LABEL+=1))
done

printf "\n"


## Valid
echo "Create val.txt..."
rm -rf $DATA/val.txt
LABEL=0
for c in ${CLASSES[@]}
do
    is_folder=1
    for i in $VAL_PATH/$c
    do
        # Process folders
        if test -d $i
        then
            find $i -name *.jpg | cut -d '/' -f 10- | sed "s/$/ ${LABEL}/" >> $DATA/val.txt
        fi

        # Process files
        if test -f $i
        then
            is_folder=0
            break
        fi
    done

    if [ $is_folder -eq 0 ]
    then
        find $VAL_PATH/$c -name *.jpg | cut -d '/' -f 10- | sed "s/$/ ${LABEL}/" >> $DATA/val.txt
    fi
    ((LABEL+=1))
done

printf "\n"


## Test
echo "Create test.txt..."
rm -rf $DATA/test.txt
LABEL=0
for c in ${CLASSES[@]}
do
    is_folder=1
    for i in $TEST_PATH/$c
    do
        # Process folders
        if test -d $i
        then
            find $i -name *.jpg | cut -d '/' -f 10- | sed "s/$/ ${LABEL}/" >> $DATA/test.txt
        fi

        # Process files
        if test -f $i
        then
            is_folder=0
            break
        fi
    done

    if [ $is_folder -eq 0 ]
    then
        find $TEST_PATH/$c -name *.jpg | cut -d '/' -f 10- | sed "s/$/ ${LABEL}/" >> $DATA/test.txt
    fi
    ((LABEL+=1))
done
printf "\n"

printf "All done! \n"
echo "train text file path = $(readlink -f "$DATA/train.txt")"
echo "val text file path = $(readlink -f "$DATA/val.txt")"
echo "test text file path = $(readlink -f "$DATA/test.txt")"
