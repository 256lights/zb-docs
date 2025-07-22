# Contributing to zb

If you're looking at contributing to the zb tool,
see the [zb contributing guide](https://github.com/256lights/zb/blob/main/CONTRIBUTING.md)
and take a look at the [issues marked as good for newcomers](https://github.com/256lights/zb/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22).

If you're looking at contributing to the standard library,
see the [standard library contributing guide](https://github.com/256lights/zb-stdlib/blob/main/CONTRIBUTING.md)
and take a look at the [issues marked as good for newcomers](https://github.com/256lights/zb-stdlib/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22).

The current public roadmap is available on [GitHub Projects](https://github.com/orgs/256lights/projects/2).

Contributors to zb must follow the [zb Code of Conduct](http://github.com/256lights/zb/blob/main/CODE_OF_CONDUCT.md).

## Improving the Documentation

This website's source is [hosted on GitHub](https://github.com/256lights/zb-docs)
and written in a superset of Markdown called [MyST][].
The website is built using [Sphinx][].
If you want to improve the docs, please feel free to submit a [pull request][].

The website is built from the [`publish` branch][],
which may lag behind the `main` branch during development.
Once zb reaches 1.0, it's likely there will not be a distinction,
but the intent is to reduce confusion for users
while features are still being developed.
Until then, the `main` branch is published at <https://main--zb-docs.netlify.app/>

[MyST]: https://myst-parser.readthedocs.io/en/latest/
[Sphinx]: https://www.sphinx-doc.org/
[`publish` branch]: https://github.com/256lights/zb-docs/tree/publish
[pull request]: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
