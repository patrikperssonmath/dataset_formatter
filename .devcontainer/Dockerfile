FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-devel

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Prevent stop building ubuntu at time zone selection.
ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm -rf /var/lib/apt/lists/*

VOLUME /database
VOLUME /workspace

# install packages
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    wget \
    git \
    unzip \
    zip \
    nano \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y libqt5gui5 mesa-utils libegl1-mesa libegl1-mesa-dev libgbm-dev libgbm1 libgl1-mesa-dev libgl1-mesa-dri libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev && \
    rm -rf /var/lib/apt/lists/*
ENV QT_DEBUG_PLUGINS=1

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

ENV GRPC_POLL_STRATEGY epoll1

ENV DEBIAN_FRONTEND=dialog

ENV PATH="${PATH}:/home/${USERNAME}/.local/bin"

RUN echo 'export PYTHONPATH=$PYTHONPATH:/workspace/thirdparty/cvgraph' >> /home/$USERNAME/.bashrc 