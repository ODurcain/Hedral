FROM python:latest

WORKDIR /Hedral
COPY libraries.txt .
RUN pip install -r libraries.txt
COPY . .
EXPOSE 5000
CMD [ "python3", "./ThreeD_Geometry.py" ]