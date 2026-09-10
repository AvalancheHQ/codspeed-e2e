# CodSpeed tokenless E2E tests

Public sample repository used by the CodSpeed platform E2E suite to validate the
**tokenless** upload path on GitHub Actions.

The tokenless flow only works on public repositories, so this repo must stay
public. Each test in `packages/api/tests/e2e/tokenless.spec.ts` opens a new pull
request that triggers a workflow run here. The workflow uploads to CodSpeed
without a token and the platform validates the run by reading the workflow logs.

The workflow runs across every supported major version of
[`CodSpeedHQ/action`](https://github.com/CodSpeedHQ/action) in a matrix so a
single PR exercises all runner versions at once.

## Dev tests

- Ensure there is a secret in this repo with the upload URL to your dev environment,
  with your name in the secret name. E.g.: `CODSPEED_JOHN_DEV_UPLOAD_URL`.
- Create a branch prefixed with your name. E.g.: john-dev/my-branch.
- Then open a PR.
