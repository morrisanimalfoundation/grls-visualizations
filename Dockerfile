FROM python:3.11
# Set environment variables
COPY requirements.txt .
ENV PYTHONPATH=\/workspace
ARG USER_ID

# Update and install necessary packages
RUN apt -y update && \
    pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir &&\
    groupadd -g 1000 jenkins && \
    useradd -l -u 503 -g jenkins -G sudo -m jenkins

# Copy the font file into the image
COPY fonts/*.otf /usr/local/share/fonts/

# Update font cache
RUN fc-cache -f -v

USER jenkins
WORKDIR /workspace