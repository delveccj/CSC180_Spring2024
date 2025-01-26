# Use a lightweight base image
FROM ubuntu:20.04

# Install SSH server
RUN apt-get update && apt-get install -y openssh-server

# Set up SSH with weak credentials
RUN mkdir /var/run/sshd && \
    echo 'root:1234' | chpasswd  # Weak root password!

# Allow root login via SSH (big no-no in production!)
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]
