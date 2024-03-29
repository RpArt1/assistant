FROM python:3.9

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r /app/requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#CMD ["python debugpy  --wait-for-client--listen 0.0.0.0:5678 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
