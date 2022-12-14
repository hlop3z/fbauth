# **Fastberry** - Authentication

## Description

Authentication **tool** for [Fastberry](https://hlop3z.github.io/fastberry/)

---

## Installation

```sh
python -m pip install fbauth
```

## Config

add file `/config/.env/development.toml`

```toml
[env]
SECRET_KEY = "fastapi-insecure-09d25e094faa6ca2556c"
```

## Database **Migration**

```sh
python manage.py db auto-migrate
```

## Create **Super User**

```sh
python manage.py create-user --super --username admin --password secret --email admin@example.com
```

## (**OR**) Create **Super User**

```sh
python manage.py create-user --super -u admin -p secret -e admin@example.com
```

## **Public** Role (Perms)

config file `/config/public-perms.json`

```json
{
  "perms": ["UserCreate", "UserLogin", "UserMe"]
}
```

## Add Middleware & Extensions

config file `/config/spoc.toml`

```toml
# [spoc] ...
[spoc.extras]
middleware = ["fbauth.middleware.AuthenticatedCookieMiddleware"]
extensions = ["fbauth.extension.InjectUser"]
permissions = ["fbauth.permissions.IsAuthorized"]
```

## GraphQL **Client**

```graphql
# User
mutation UserCreate {
  UserCreate(
    form: {
      password: "my-secret-password"
      username: "John-Doe"
      email: "johndoe@example.com"
    }
  ) {
    ... on User {
      ...UserFields
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

mutation UserLogin {
  UserLogin(
    username: null
    email: "johndoe@example.com"
    password: "my-secret-password"
  ) {
    ... on AccessToken {
      token
      tokenType
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

mutation AdminLogin {
  UserLogin(username: "admin", password: "secret") {
    ... on AccessToken {
      token
      tokenType
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

mutation UserUpdate {
  UserUpdate(form: { password: null, email: null, username: "John-Doe" }) {
    ... on User {
      ...UserFields
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

mutation UserRefreshToken {
  UserRefreshToken(token: null) {
    token
    tokenType
  }
}

mutation UserDisable {
  UserDisable(state: false)
}

query UserMe {
  UserMe {
    ...UserFields
  }
}

query UserDetail {
  UserDetail(id: "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==") {
    ...UserFields
  }
}

# Roles

query AllRoles {
  RoleAll {
    id
    name
    perms
  }
}

mutation CreateRole {
  RoleCreate(form: { name: "enduser", perms: null }) {
    ... on Role {
      id
      name
      perms
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

mutation UpdateRole {
  RoleUpdate(
    form: {
      id: "MTo6YTU1ZTUzMmVhYjAyOGI0Mg=="
      name: "manager"
      perms: ["AllRoles"]
    }
  ) {
    ... on Role {
      id
      name
      perms
    }
    ... on Error {
      ...ErrorFields
    }
  }
}

mutation DeleteRole {
  RoleDelete(id: "MTo6YTU1ZTUzMmVhYjAyOGI0Mg==")
}

# Reusable

fragment ErrorFields on Error {
  error
  meta
  messages {
    field
    text
    type
  }
}

fragment UserFields on User {
  id
  username
  email
  password
  isDisabled
  isStaff
  isSuperUser
  isAuthenticated
  isAnonymous
  createdOn
  role {
    id
    name
    perms
  }
}
```
