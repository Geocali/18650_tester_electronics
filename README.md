# 18650_tester_electronics
Electronics for the 18650_tester project

Build the Docker image:
docker build . -t ngspice

Run the image:
docker run -it -v $(pwd):/home ngspice /bin/bash