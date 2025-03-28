FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

WORKDIR /workspace

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD src/rp_handler.py ./

CMD ["python", "rp_handler.py"]