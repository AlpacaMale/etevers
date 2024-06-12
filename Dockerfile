FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]





# flask 젠킨스 Dokerfile pipeline 
# Use the official image as a parent image.
FROM node:current-slim

# Set the working directory
WORKDIR /home

# Copy the file from your host to your current location.
COPY app/ /home/

# Run the command inside your image filesystem
RUN npm install

# Inform Docker that the container is listening on the specified port at runtime
EXPOSE 3000

# Run the specified command within the container.
CMD ["npm", "start"]

# Copy the rest of your app's source code from your host to your image filesystem.
