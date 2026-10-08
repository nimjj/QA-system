FROM node:20-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy rest of the frontend code
COPY . .

# Expose Vite's default port
EXPOSE 5173

# Run the dev server and bind to 0.0.0.0 so it's accessible from the host
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
