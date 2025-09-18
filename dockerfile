FROM rust:latest AS builder
WORKDIR /app
COPY . .
RUN cargo install --path .

FROM public.ecr.aws/lambda/python:3.11
COPY --from=builder /usr/local/cargo/bin/check_if_email_exists /usr/local/bin/check_if_email_exists

# We will use a proxy to call the binary.
COPY proxy.py .

CMD ["proxy.py"]