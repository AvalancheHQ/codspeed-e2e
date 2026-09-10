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

Then trigger the dev job either way:

- **From a PR:** create a branch prefixed with your name (e.g. `john-dev/my-branch`)
  and open a PR. The `<slug>-dev/` prefix selects your secret.
- **From `main`:** run the workflow manually (Actions → benchmarks → Run workflow,
  or `gh workflow run codspeed.yml -f dev_slug=john`) with the `dev_slug` input set
  to your slug. A dev dispatch runs only the dev job; leaving `dev_slug` empty runs
  the staging and prod jobs instead.
