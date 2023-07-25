FROM python:3.11

RUN python3 -m pip install --extra-index-url https://test.pypi.org/simple/ gpyt_commandbus==0.0.7
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic
COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

CMD ["./entrypoint.sh"]
