# Local development image for the Next.js frontend (used by docker-compose.yml).
# Vercel builds the frontend natively from frontend/; this file is not used there.
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
