FROM public.ecr.aws/lambda/python:3.8

COPY . /var/task/
COPY lambda_handler.py .
COPY profile_profiler.py .
COPY jt_sql_alt.py .
COPY requirements.txt .
COPY prompt.txt .
COPY dlc_names_dict.json .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["lambda_handler.run_profile"]
