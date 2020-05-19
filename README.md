# 18650_tester_electronics
Electronics for the 18650_tester project

Build the Docker image:
docker build . -t ngspice

Run the image:
docker run -it -v $(pwd):/home -p 8888:8888 ngspice /bin/bash

jupyter lab --ip=0.0.0.0 --no-browser --allow-root

Process:
- create circuit in PySpice with python objects
- export netlist
- import in Kicad and place the elements
- export the PDF from Kicad