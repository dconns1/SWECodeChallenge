FROM debian:12

# Install Dependencies
RUN apt-get update && apt-get install -y \
    sudo \
    debhelper \
    dh-python \
    python3-pip

# Create Users
RUN useradd -m -G sudo -s /bin/bash testUser \
    && echo testUser ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/testUser \
    && chmod 0440 /etc/sudoers.d/testUser

# Create working directory
RUN mkdir /var/SWE

# Set the working directory
WORKDIR /var/SWE

# Copy the application code
COPY . /var/SWE