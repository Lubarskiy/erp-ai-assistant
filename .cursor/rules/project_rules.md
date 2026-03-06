# Project Rules

## Архитектура
- Backend разделяется на слои: api, services, repositories, integrations
- Запрещено писать SQL в API
- Запрещено писать бизнес-логику в endpoints

## Работа с LLM
- LLM не имеет прямого доступа к ERP
- LLM используется только для intent classification, explanation и RAG
- Запрещено передавать ИНН, номера документов, персональные данные

## Работа с 1С
- Доступ к 1С только через integrations/onec
- Нельзя вызывать 1С из chat_service, api endpoints, rag_service

## Качество
- Изменения делать маленькими шагами
- После каждого шага запускать tests
- Не переписывать работающие модули без необходимости
