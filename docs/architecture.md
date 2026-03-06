# ERP AI Assistant Architecture

## Цель MVP
AI-ассистент для 1С:Предприятие с FastAPI backend, PostgreSQL, pgvector, JWT, Docker Compose и интеграцией через OData + HTTP-сервисы.

## Слои
- api
- services
- repositories
- integrations
- database

## Ключевые модули
- chat/orchestrator
- intent-service
- analytics-service
- rag-service
- 1C connector
- sync/ETL
- audit
- knowledge base

## Правила
- API не содержит SQL
- бизнес-логика не живет в endpoints
- прямой доступ к 1С только в integrations/onec
- LLM не получает ИНН, номера документов и персональные данные
