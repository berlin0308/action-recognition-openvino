FROM tensorflow/tensorflow:2.9.0-gpu

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y python3.8 python3.8-dev python3.8-distutils curl ffmpeg \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.8 get-pip.py \
    && rm get-pip.py \
    && apt clean

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.8 1

RUN pip install nvitop progressbar2 tf-models-official==2.9.0 tensorflow-addons==0.17.0 moviepy mediapy
