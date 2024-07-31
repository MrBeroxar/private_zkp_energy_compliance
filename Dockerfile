# Use the Python base image
FROM python:3.8-slim as app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install the official ZoKrates using its installation script
RUN curl -LSfs get.zokrat.es | sh

# Clone the Bachelor-Thesis repository, which includes ZoKrates as a submodule
WORKDIR /usr/src
RUN git clone --recursive https://github.com/uZhW8Rgl/Bachelor-Thesis.git

# Build the custom ZoKrates from the Bachelor-Thesis submodule
WORKDIR /usr/src/Bachelor-Thesis/ZoKrates
RUN cargo build --release --package zokrates_cli

# Add both the official and custom ZoKrates binaries to the PATH, with priority given to the custom version
ENV PATH="/usr/src/Bachelor-Thesis/ZoKrates/target/release:${PATH}"
ENV ZOKRATES_STDLIB="/usr/src/Bachelor-Thesis/ZoKrates/zokrates_stdlib/stdlib"

# Set the work directory for the Python app
WORKDIR /app

# Copy the Python requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Command to run the application
CMD ["python", "./src/proof_of_compliance/MockVerifier.py"]
