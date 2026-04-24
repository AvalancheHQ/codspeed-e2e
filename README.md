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
