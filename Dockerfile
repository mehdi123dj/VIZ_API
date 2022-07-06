FROM python:3.10.4

ENV DASH_DEBUG_MODE True
WORKDIR /usr/src/app

# Copy and install packages
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Copy app folder to app folder in container
COPY /visualization /usr/src/app/

# Changing to non-root user
RUN useradd -m appUser
USER appUser

CMD ["python", "visualization.py"]