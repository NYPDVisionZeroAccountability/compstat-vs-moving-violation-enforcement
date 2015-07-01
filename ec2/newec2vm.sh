#!/bin/bash
BASEDIR=$(dirname $0)
my_user_data=`cat $BASEDIR/vm.yml`
aws ec2 run-instances \
    --image-id        ami-9eaa1cf6 \
    --count           1 \
    --instance-type   t2.micro \
    --key-name        NYPDVisionZeroAccountability \
    --security-groups web altssh \
    --user-data       "$my_user_data"
