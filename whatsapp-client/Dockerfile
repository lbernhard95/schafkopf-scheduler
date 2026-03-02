# ============================================
# Use AWS Lambda Adapter to convert HTTP requests to Lambda events
# ============================================
FROM public.ecr.aws/awsguru/aws-lambda-adapter:0.9.0 AS aws-lambda-adapter

# ============================================
# Use official Bun image with Debian base
# ============================================
FROM oven/bun:debian AS runtime

# Copy the Lambda adapter into the container
COPY --from=aws-lambda-adapter /lambda-adapter /opt/extensions/lambda-adapter

# Set the port to 8080 (required for AWS Lambda adapter)
ENV PORT=8080

# Set work directory to Lambda's task root
WORKDIR /var/task

# Copy package files and install dependencies
COPY package.json bun.lock* ./
RUN bun install --production --frozen-lockfile

# Copy application source code
COPY src ./src
COPY tsconfig.json ./

# Create tmp directory for WhatsApp auth files
RUN mkdir -p tmp/auth

# Run the HTTP server with Bun
# Lambda Adapter will convert Lambda events to HTTP requests
CMD ["bun", "src/lambda-server.ts"]
