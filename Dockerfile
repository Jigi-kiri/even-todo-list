From python:3.12
WORKDIR /app
COPY . /app
CMD ["python", "./todo_cli.py"]