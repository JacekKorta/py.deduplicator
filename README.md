# py.deduplicator
<a href="https://www.repostatus.org/#wip"><img src="https://www.repostatus.org/badges/latest/wip.svg" alt="Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public." /></a><br>

This service is a part of the repo: [microservices-training-ground](https://github.com/JacekKorta/microservices-training-ground)<br>
Service py.deduplicator is responsible for deduplication. This service reads messages from the queue, checks their id in RedisDB and if the id exists the message is dropped. Otherwise the message is sent to exchange for deduplicated messages and the ID of message is saved in DB

### How to run?

You should run this service via docker compose in main repo [microservices-training-ground](https://github.com/JacekKorta/microservices-training-ground)

Create env file:

```bash
cp .env.exaample .env
```
You can leave .env unchanged