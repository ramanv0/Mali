FROM python:3.6-slim
COPY ./app.py /mali/
COPY ./features.py /mali/
COPY ./requirements.txt /mali/
COPY ./predictor.pkl /mali/
COPY ./dataset/bodmas_malware_category.csv /mali/
WORKDIR /mali/
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]