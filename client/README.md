[![CodeCov](https://codecov.io/github/yunity/karrot-frontend/coverage.svg)](https://codecov.io/gh/yunity/karrot-frontend)
[![CircleCI](https://circleci.com/gh/yunity/karrot-frontend.svg?style=shield)](https://circleci.com/gh/yunity/karrot-frontend)
[![Known Vulnerabilities](https://snyk.io/test/github/yunity/karrot-frontend/e4f6927cccfbde340636d20b863efd508be19ec0/badge.svg)](https://snyk.io/test/github/yunity/karrot-frontend/e4f6927cccfbde340636d20b863efd508be19ec0)


# karrot frontend

This is the frontend repository, i.e. the browser-side software that powers [foodsaving worldwide](https://karrot.world).

# Setup

## Requirements

- [Node.js](https://nodejs.org/) and [yarn](https://yarnpkg.com/en/docs/install)

To clone and install:

```
git clone https://github.com/yunity/karrot-frontend.git
cd karrot-frontend
yarn
```

To run the local dev server:

```
yarn dev
```

To lint and run the tests:

```
yarn lint
yarn test
```

If you want to use an eslint plugin for your editor, please keep in mind that you either have to install all eslint plugins listed in package.json globally or you run `yarn install`. Otherwise your eslint plugin may not work.

# Start contributing?

Be sure to join us in the #karrot-dev [chatroom on slack](https://slackin.yunity.org/) and get in contact!
The most important information are written down in our [contribution guidelines](CONTRIBUTE.md).

The [backend](https://github.com/yunity/karrot-backend) is developed to support this frontend. If you find a bug or miss something in the API, please file an issue in the backend repository.
