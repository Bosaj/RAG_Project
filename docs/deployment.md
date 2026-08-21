# Deployment Guide

## Docker Compose
`ash
docker compose -f docker/docker.compose.yml up -d
`

## Docker Container Run
`ash
docker build -f docker/Dockerfile -t rag-api:latest .
docker run -d --name rag-engine -p 5000:5000 --env-file src/.env rag-api:latest
`
