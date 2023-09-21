FROM python:3.9-alpine

# Create necessary directories and files
RUN mkdir ~/.snipsave/ && \
    touch ~/.snipsave/credentials && \
    echo "alias ssv='python3 /opt/main.py'" >> ~/.bashrc

# Create a global ssv command
RUN echo '#!/bin/sh' > /usr/bin/ssv && \
    echo 'exec python3 /opt/main.py "$@"' >> /usr/bin/ssv && \
    chmod +x /usr/bin/ssv

COPY ./requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt

# Copy your CLI Python script
COPY ./src /opt

# Create a startup script to display the welcome message and source the profile
RUN echo '#!/bin/sh' > /welcome.sh && \
    echo 'echo "-----------------------------"' >> /welcome.sh && \
    echo 'echo ""' >> /welcome.sh && \
    echo 'echo "Welcome to SnipSave CLI!"' >> /welcome.sh && \
    echo 'echo ""' >> /welcome.sh && \
    echo 'echo "To add your credentials to"' >> /welcome.sh && \
    echo 'echo "the CLI, type:"' >> /welcome.sh && \
    echo 'echo ""' >> /welcome.sh && \
    echo 'echo "$ ssv configure"' >> /welcome.sh && \
    echo 'echo ""' >> /welcome.sh && \
    echo 'echo "Or, check out the our"' >> /welcome.sh && \
    echo 'echo "documentation at"' >> /welcome.sh && \
    echo 'echo "https://github.com/SnipSaveCLI/SnipSaveCLI/blob/main/README.md"' >> /welcome.sh && \
    echo 'echo ""' >> /welcome.sh && \
    echo 'echo "-----------------------------"' >> /welcome.sh && \
    echo 'exec /bin/sh' >> /welcome.sh && \
    chmod +x /welcome.sh

# Start the shell with the welcome script
CMD ["/welcome.sh"]
