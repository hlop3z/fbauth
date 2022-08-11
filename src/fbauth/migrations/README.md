# SQL-Alchemy Migrations

## Make-Migrations

```sh
alembic revision -m "migration message"
```

## Make-Migrations (Auto-Generate)

```sh
alembic revision --autogenerate -m "migration message"
```

## Migrate

```sh
alembic upgrade head
```

## History

```sh
alembic history
```

---

# Relative Migration Identifiers

## Upgrade

```sh
alembic upgrade +2
```

## Downgrade

```sh
alembic upgrade -1
```
