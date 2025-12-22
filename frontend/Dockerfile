# Usamos Node 22 (LTS más reciente) para compatibilidad con Vite 7
FROM node:22-alpine

WORKDIR /app

# Activamos pnpm nativo (viene con Node, solo hay que encenderlo)
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copiamos package.json Y el archivo de bloqueo de pnpm
COPY package.json pnpm-lock.yaml ./

# Instalamos dependencias usando pnpm
RUN pnpm install

# Copiamos el código fuente
COPY . .

# Exponemos el puerto de Vite
EXPOSE 5173

# Levantamos el servidor de desarrollo
CMD ["pnpm", "dev", "--host"]