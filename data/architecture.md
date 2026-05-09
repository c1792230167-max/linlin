# System Architecture

系统采用微服务架构：

- user-service
- order-service
- payment-service

服务间通过 Kafka 通信。
数据库使用 PostgreSQL。
缓存使用 Redis。
