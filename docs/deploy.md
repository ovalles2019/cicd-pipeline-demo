# Wiring real deploys

The GitHub Actions workflow always builds, tests, scans, and (on `main`) pushes
an image to **GHCR**. Deploy jobs promote through GitHub Environments and
redeploy the matching Render service.

## 1. Create GitHub Environments

Repo → **Settings → Environments** → create:

| Environment | Protection |
|-------------|------------|
| `qa` | none (auto-deploy on main) |
| `staging` | Required reviewers: you |
| `production` | Required reviewers: you |

Optional environment variables (shown as the job URL in Actions):

- `QA_URL`
- `STAGING_URL`
- `PRODUCTION_URL`

## 2. Deploy the Render Blueprint (or create via API)

**Option A — Blueprint**

1. Merge to `main`.
2. In [Render](https://dashboard.render.com): **New → Blueprint** → select this repo.
3. Confirm the three services from `render.yaml`.

**Option B — already created**

Service IDs are stored as repository variables:

| Variable | Service |
|----------|---------|
| `RENDER_SERVICE_ID_QA` | cicd-demo-qa |
| `RENDER_SERVICE_ID_STAGING` | cicd-demo-staging |
| `RENDER_SERVICE_ID_PRODUCTION` | cicd-demo-production |

## 3. Authenticate deploys (pick one)

### Deploy Hooks (simplest)

For each Render service: **Settings → Deploy Hook → Copy**.

GitHub → **Settings → Secrets and variables → Actions**:

| Secret | Service |
|--------|---------|
| `RENDER_DEPLOY_HOOK_QA` | cicd-demo-qa |
| `RENDER_DEPLOY_HOOK_STAGING` | cicd-demo-staging |
| `RENDER_DEPLOY_HOOK_PRODUCTION` | cicd-demo-production |

### Render API key (alternative)

1. Create an API key in Render → Account Settings → API Keys.
2. Add repo secret `RENDER_API_KEY`.
3. Ensure the three `RENDER_SERVICE_ID_*` repository variables are set.

Deploy jobs try Deploy Hook first, then fall back to the API.

## 4. GHCR

Images land at `ghcr.io/<owner>/cicd-pipeline-demo` (`:sha`, `:qa`, `:latest`).

## 5. Promotion path

```
main merge
  → release pushes :sha, :qa, :latest to GHCR
  → deploy-qa (auto)
  → deploy-staging (waits for your approval)
  → deploy-production (waits for your approval)
```

Without Render credentials, deploy jobs still succeed and *simulate* promotion
so you can learn the Actions graph first.
