# Base image
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install necessary services
RUN apt-get update && apt-get install -y \
    apache2 \
    mysql-server \
    vsftpd \
    openssh-server \
    iputils-ping \
    net-tools \
    && apt-get clean

# Enable Apache and MySQL to start at boot
RUN systemctl enable apache2 && systemctl enable mysql

# Set up SSH (default password for root is 'root' for testing purposes)
RUN mkdir /var/run/sshd && echo 'root:root' | chpasswd
EXPOSE 22 80 3306 21

# Start necessary services when the container starts
CMD service apache2 start && service mysql start && service vsftpd start && /usr/sbin/sshd -D

