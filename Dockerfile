FROM python:3.10.4

ENV DASH_DEBUG_MODE True
COPY /visualization
WORKDIR /app
RUN set -ex && \
    pip install -r requirements.txt
EXPOSE 8050
CMD ["python", "visualization.py"]