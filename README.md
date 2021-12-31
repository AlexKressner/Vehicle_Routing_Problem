# Vehicle_Routing_Problem

## Info
A simple example notebook that uses [Google OR-Tools](https://developers.google.com/optimization/routing) to solve instances of the [Solomon benchmark](https://www.sintef.no/projectweb/top/vrptw/solomon-benchmark/100-customers/) (vehicle routing problem with time windows).

## Usage
Make sure [Docker](https://www.docker.com) is installed.

1. Clone repo
  ```sh
    git clone https://github.com/AlexKressner/Vehicle_Routing_Problem
  ```
2. Change directory
  ```sh
    cd Vehicle_Routing_Problem
  ```
3. Build and launch with docker
  ```sh
    docker build -t vrp:latest .
    docker run -p 8888:8888 vrp 
  ```
4. Copy and paste URL from terminal in browser to open the notebook (``http://127.0.0.1:8888/...``)