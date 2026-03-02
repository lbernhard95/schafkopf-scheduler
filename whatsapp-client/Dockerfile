# Use the official AWS Lambda Node.js 22 image
# This includes the Lambda Runtime Interface Client (RIC) built-in
FROM public.ecr.aws/lambda/nodejs:22

# Install Bun runtime
RUN curl -fsSL https://bun.sh/install | bash -s -- bun-v1.1.38 && \
    ln -s /root/.bun/bin/bun /usr/local/bin/bun

# Set work directory to Lambda's task root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy package files
COPY package.json bun.lock* ./

# Install dependencies with Bun
RUN bun install --production --frozen-lockfile

# Copy application code
COPY src ./src
COPY config ./config
COPY tsconfig.json ./

# Set the CMD to the Lambda handler
# Bun can run TypeScript directly, no transpilation needed!
CMD ["bun", "run", "src/lambda.ts"]
