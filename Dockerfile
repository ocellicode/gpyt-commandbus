FROM python:3.11

RUN python3 -m pip install --index-url https://test.pypi.org/simple/ gpyt_commandbus==0.0.1

CMD ["waitress-serve", "gpyt_commandbus.injection.injector:app"]
