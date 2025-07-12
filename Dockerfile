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

RUN curl -sSL https://raw.githubusercontent.com/brunoribeiro-lab/ffmpeg-7.0.2-amd64-static/main/ffmpeg \
      -o /usr/local/bin/ffmpeg && \
    curl -sSL https://raw.githubusercontent.com/brunoribeiro-lab/ffmpeg-7.0.2-amd64-static/main/ffprobe \
      -o /usr/local/bin/ffprobe && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe

COPY . ${LAMBDA_TASK_ROOT}/

CMD ["lambda_function.lambda_handler"]