#! /bin/bash

if [[ $2 != "stg" && $2 != "pro" ]]; then
  echo ">>> Please input [stg | pro]"
  exit 1;
fi

name=cdd-admin-$1-$2

echo ">>> Building new image"
docker build -t $name -f Dockerfile .

echo ">>> Stopping old container"
docker stop $name

echo ">>> Removing old container"
docker rm -f $name

echo ">>> Running new container"
if [ $1 = "srv" ]; then
  docker run --name $name -e ENV=$2 -e SERVICE=$1 \
  --dns=183.60.83.19 --dns=223.5.5.5 --restart=always \
  -v /home/oper/docker/$name/logs:/home/app/logs \
  -v /home/tonnn/workspace/uploads/img:/home/app/temp/img \
  -v /home/tonnn/workspace/uploads/apk:/home/app/temp/apk \
  -p 8000:80 -d $name
else
  docker run --name $name -e ENV=$2 -e SERVICE=$1 \
  --dns=183.60.83.19 --dns=223.5.5.5 --restart=always \
  -v /home/oper/docker/$name/logs:/home/app/logs \
  -d $name
fi

echo ">>> Removing exited container"
docker ps -a | grep Exited | awk '{ print $1 }' | while read -r id ; do
  docker rm $id
done

echo ">>> Cleaning up images"
docker images | grep "<none>" | awk '{ print $3 }' | while read -r id ; do
  docker rmi $id
done
