# 
FROM python:latest
WORKDIR /Hedral
COPY libraries.txt .
RUN pip install -r libraries.txt
COPY . .
EXPOSE 5000

# Set the entry point
COPY Docker_Entry.sh /Docker_Entry.sh
RUN chmod +x /Docker_Entry.sh
ENTRYPOINT [ "/Docker_Entry.sh" ]
