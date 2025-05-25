FROM public.ecr.aws/lambda/python:3.13

COPY torsocks-2.4.0-1.fc36.x86_64.rpm /tmp/
RUN rpm -Uvh /tmp/torsocks-2.4.0-1.fc36.x86_64.rpm
COPY torproject.repo /etc/yum.repos.d/
RUN dnf install -y --setopt=install_weak_deps=0 tor
RUN ln -sf /usr/bin/tor ${LAMBDA_TASK_ROOT}
RUN pip install PySocks
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
CMD [ "lambda_function.lambda_handler" ]
