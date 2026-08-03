# Wiring real deploys (optional — pipeline works without this)

The GitHub Actions workflow always builds, tests, and (on `main`) pushes
an image to **GHCR**. Deploy jobs call Render Deploy Hooks when secrets exist;
otherwise they print a simulated promotion so you can learn the flow first.

## 1. Create GitHub Environments

Repo → **Settings → Environments** → create:

| Environment | Protection |
|-------------|------------|
| `qa` | none (auto-deploy on main) |
| `staging` | Required reviewers: you |
| `production` | Required reviewers: you |

Optional environment variables (shown as the job URL in Actions):

- `QA_URL` → `https://cicd-demo-qa.onrender.com`
- `STAGING_URL` → `https://cicd-demo-staging.onrender.com`
- `PRODUCTION_URL` → `https://cicd-demo-production.onrender.com`

## 2. Deploy the Render Blueprint

1. Push this repo to GitHub.
2. In [Render](https://dashboard.render.com): **New → Blueprint** → select the repo.
3. Confirm the three services from `render.yaml`.

## 3. Add Deploy Hook secrets

For each Render service: **Settings → Deploy Hook → Copy**.

GitHub → **Settings → Secrets and variables → Actions**:

| Secret | Service |
|--------|---------|
| `RENDER_DEPLOY_HOOK_QA` | cicd-demo-qa |
| `RENDER_DEPLOY_HOOK_STAGING` | cicd-demo-staging |
| `RENDER_DEPLOY_HOOK_PRODUCTION` | cicd-demo-production |

## 4. GHCR visibility

Images land at `ghcr.io/<owner>/cicd-pipeline-demo`.

If Render pulls from GHCR and the package is private, create a
[Render registry credential](https://render.com/docs/deploying-an-image#credentials)
with a GitHub PAT that has `read:packages`.

For a public demo, set the package to **Public** under
GitHub → Packages → package settings.

## 5. Promotion path

```
main merge
  → release pushes :sha, :qa, :latest to GHCR
  → deploy-qa (auto)
  → deploy-staging (waits for your approval)
  → deploy-production (waits for your approval)
```

Each deploy job hits the matching Render hook, which rebuilds/redeploys
that environment's service from this repo's Dockerfile.
