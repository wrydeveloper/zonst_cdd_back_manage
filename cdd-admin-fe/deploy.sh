#! /bin/bash

if [[ $1 != "stg" && $1 != "pro" ]]; then
  echo ">>> Please input [stg | pro]"
  exit 1;
fi

# cnpm install
# npm run $1

name=cdd-admin-fe-$1

echo '>>> Building new image'
docker build --no-cache -t $name -f Dockerfile .

echo ">>> Stopping old container"
docker stop $name

echo ">>> Removing old container"
docker rm -f $name

echo ">>> Running new container"
docker run --name $name --dns=223.5.5.5 -p 8081:80 -d $name

echo ">>> Removing exited container"
docker ps -a | grep Exited | awk '{ print $1 }' | while read -r id ; do
  docker rm $id
done

echo '>>> Cleaning up images'
docker images | grep "<none>" | awk '{ print $3 }'  | while read -r id ; do
  docker rmi $id
done
