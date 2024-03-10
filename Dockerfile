FROM python:latest

WORKDIR /Hedral
COPY libraries.txt .
RUN pip install -r libraries.txt
COPY . .
EXPOSE 5000
#  runs the python progrem
# To-Do: put you in the hedral env automatically (can only kind of do this)
CMD [ "python3","src/main/ThreeD_Geometry.py" ]