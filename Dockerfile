FROM public.ecr.aws/lambda/python:3.12

RUN pip install --upgrade pip wheel

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ${LAMBDA_TASK_ROOT}/

CMD ["lambda_function.lambda_handler"]