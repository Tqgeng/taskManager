FROM python:3.11.12-bullseye

WORKDIR /myProjectTaskManager

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x prestart.sh

ENTRYPOINT ["./prestart.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]