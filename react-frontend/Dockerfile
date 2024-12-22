FROM node:20

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Expose both potential ports
EXPOSE 5173
EXPOSE 4173

# Start the development server with host flag
CMD ["npm", "run", "dev", "--", "--host"]