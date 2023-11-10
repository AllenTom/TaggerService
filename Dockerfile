
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime
# Installing python dependencies
RUN python3 -m pip --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    python3 --version && \
    pip3 --version

COPY ./requirements.txt .
RUN pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn
# Copy model files
COPY ./ /app

# Copy app files
WORKDIR /app
ENV PYTHONPATH=/app
RUN ls -lah /app/*

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000
CMD ["/start.sh"]