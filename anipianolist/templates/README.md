Templates in these folders can be accessed globally by URL routing.

- **account** and **socialaccount** override default templates from `django-allauth`
- **core** are globally used template snippets

For templates relating to individual apps, you're probably looking for `$ROOT/anipianolist/[accounts||base]/templates/[accounts||base]`

Note that `accounts` is an **anipianolist** app, whereas `account` is a `django-allauth` app.