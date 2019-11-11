FROM python:3
COPY src/main.py /
COPY src/lsystem.py /
COPY src/graphics/* /graphics/
RUN chmod 755 main.py
ENTRYPOINT ["python", "main.py"]
CMD []

