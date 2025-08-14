FROM node:18-alpine

# Set work directory
WORKDIR /app

# Set environment variables
ENV NODE_ENV=production
ENV CI=true

# Copy package files
COPY package*.json ./

# Install dependencies with better error handling
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Build the application with better error handling
RUN npm run build

# Install serve for production
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Start production server
CMD ["serve", "-s", "dist", "-l", "3000"] 