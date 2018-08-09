#!/bin/bash

if [ "$#" -ne 2 ]; then
   echo "Usage:  ./init.sh bucket-name folder-name"
   exit
fi

BUCKET=$1
FOLDER=$2
echo "creating dataproc computing cluster"

gcloud dataproc clusters create my-cluster --zone us-central1-a \
	--master-machine-type n1-standard-1 --master-boot-disk-size 50 \
	--num-workers 2 --worker-machine-type n1-standard-1 \
	--worker-boot-disk-size 50 --network=default \

echo "copying py stuff to cloud storage bucket gs://$BUCKET/$FOLDER"

gsutil -m cp *.py gs://$BUCKET/$FOLDER
gsutil -m setmeta -h "Content-Type:text/plain" gs://$BUCKET/$FOLDER/*.py

echo "done"
