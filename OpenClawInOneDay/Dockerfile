FROM node:24-bullseye

RUN apt-get update && apt-get install -y \
    git curl python3 build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g openclaw

WORKDIR /app

VOLUME ["/root/.openclaw"]

EXPOSE 18789

ENTRYPOINT ["openclaw"]
CMD ["gateway"]