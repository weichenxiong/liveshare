#!/bin/bash

 # 启动容器
function startFastDFS() {
    sudo docker start 4ce 151 6ed
    sleep 1s
    ls
    sudo docker exec -it 4ce bash
}
startFastDFS
