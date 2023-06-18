FROM python:slim
WORKDIR /opt
RUN apt update && apt install -y make git build-essential libgl1-mesa-glx
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH='/opt'
RUN apt install -y libglib2.0-0
CMD ["python", "app/bot.py"]$