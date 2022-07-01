FROM python:3.10

ENV DASH_DEBUG_MODE True
COPY ./Visualization /Visualization
WORKDIR /visualization
RUN set -ex && \
    pip install -r ./Config/requirements.txt
EXPOSE 8050
CMD ["python", "visualization.py"]