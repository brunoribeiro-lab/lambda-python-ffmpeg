FROM public.ecr.aws/lambda/python:3.12

ENV DNF_OPTS="-y --nodocs"

RUN dnf update $DNF_OPTS && \
    dnf install $DNF_OPTS \
        tar \
        xz \
        curl-minimal \
    && dnf clean all

RUN pip install --upgrade pip wheel
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    | tar -xJ -C /tmp --strip-components=1 ffmpeg-*-static && \
    mv /tmp/ffmpeg /usr/local/bin/ffmpeg && \
    mv /tmp/ffprobe /usr/local/bin/ffprobe && \
    rm -rf /tmp

COPY . ${LAMBDA_TASK_ROOT}/

CMD ["lambda_function.lambda_handler"]