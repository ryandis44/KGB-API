FROM python:3.12

# Set the working directory
WORKDIR /home/container

# Install git
RUN apt-get update && apt-get install -y git

RUN rm -rf /home/container/*

# Command to run the app using uvicorn
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000

# Clone repo, install requirements, and start API
CMD ["sh", "-c", "git clone --branch $BRANCH $GIT_ADDRESS.git /home/container && pip install -r /home/container/requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8000"]