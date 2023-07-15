#Used to create the base image for challenges
FROM ubuntu:jammy-20230624
RUN apt-get update -y && apt-get install gcc-11 g++-11 python3-pip -y
RUN CMAKE_ARGS="-DLLAMA_OPENBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python==0.1.48 --no-cache-dir