FROM public.ecr.aws/lambda/python:3.13

RUN dnf install -y libevent
RUN pip install PySocks
COPY --chown=root:root tor ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
CMD [ "lambda_function.lambda_handler" ]
