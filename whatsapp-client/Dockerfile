# ============================================
# STAGE 1: Builder - Use Bun to bundle TypeScript
# ============================================
FROM public.ecr.aws/lambda/nodejs:22 AS builder

# Install unzip (required for Bun installer) and Bun runtime
RUN dnf install -y unzip && \
    curl -fsSL https://bun.sh/install | bash -s -- bun-v1.1.38 && \
    ln -s /root/.bun/bin/bun /usr/local/bin/bun && \
    dnf clean all

# Set working directory
WORKDIR /build

# Copy package files and install all dependencies (including dev dependencies for bundling)
COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile

# Copy application source code
COPY src ./src
COPY tsconfig.json ./

# Bundle TypeScript to JavaScript with all dependencies
# This creates a single index.js file with everything bundled in CommonJS format
RUN bun build src/lambda.ts \
    --target=node \
    --outfile=dist/index.js \
    --format=cjs \
    --minify \
    --sourcemap

# ============================================
# STAGE 2: Runtime - AWS Lambda Node.js base
# ============================================
FROM public.ecr.aws/lambda/nodejs:22

# Set work directory to Lambda's task root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy only the bundled JavaScript from builder
COPY --from=builder /build/dist/index.js ./

# Set the CMD to the Lambda handler in standard format
# Lambda will invoke: index.handler()
CMD ["index.handler"]
