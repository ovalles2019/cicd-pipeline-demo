# Wiring real deploys

The GitHub Actions workflow always builds, tests, scans, and (on `main`) pushes
an image to **GHCR**. Deploy jobs promote through GitHub Environments and tell
Render to **pull that registry image** (not rebuild from git).

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

## 2. Deploy the Render Blueprint (image-backed services)

`render.yaml` defines three **`runtime: image`** web services that pull from
`ghcr.io/ovalles2019/cicd-pipeline-demo` (`:qa` for QA/Staging, `:latest` for
Production). There is no `pip install` / source build on Render — the artifact
is the image CI already published.

**Option A — Blueprint**

1. Merge to `main` (so GHCR has at least one tag Render can resolve).
2. In [Render](https://dashboard.render.com): **New → Blueprint** → select this repo.
3. Confirm the three services from `render.yaml`.

**Option B — already created**

Service IDs are stored as repository variables:

| Variable | Service |
|----------|---------|
| `RENDER_SERVICE_ID_QA` | cicd-demo-qa |
| `RENDER_SERVICE_ID_STAGING` | cicd-demo-staging |
| `RENDER_SERVICE_ID_PRODUCTION` | cicd-demo-production |

> **Note:** `runtime` is immutable. If you previously created these as native
> Python (`pip install`) services, delete them and re-apply the Blueprint so
> they are image-backed.

### Private GHCR packages

If the package is private, add a **Registry Credential** in Render (GitHub PAT
with `read:packages`), name it `ghcr-credentials`, and uncomment `image.creds`
in `render.yaml`.

## 3. Authenticate deploys (pick one)

### Deploy Hooks (simplest)

For each Render service: **Settings → Deploy Hook → Copy**.

GitHub → **Settings → Secrets and variables → Actions**:

| Secret | Service |
|--------|---------|
| `RENDER_DEPLOY_HOOK_QA` | cicd-demo-qa |
| `RENDER_DEPLOY_HOOK_STAGING` | cicd-demo-staging |
| `RENDER_DEPLOY_HOOK_PRODUCTION` | cicd-demo-production |

Deploy jobs append `imgURL=<ghcr ref>` so Render pulls the promoted tag
(e.g. `:sha`, `:qa`, `:latest`) instead of only redeploying the Blueprint default.

### Render API key (alternative)

1. Create an API key in Render → Account Settings → API Keys.
2. Add repo secret `RENDER_API_KEY`.
3. Ensure the three `RENDER_SERVICE_ID_*` repository variables are set.

Deploy jobs try Deploy Hook first, then fall back to
`POST /v1/services/{id}/deploys` with `{"imageUrl":"..."}`.

## 4. GHCR

Images land at `ghcr.io/<owner>/cicd-pipeline-demo` (`:sha`, `:qa`, `:latest`).

## 5. Promotion path

```
main merge
  → release pushes :sha, :qa, :latest to GHCR
  → deploy-qa pulls :sha into cicd-demo-qa
  → deploy-staging pulls :qa into cicd-demo-staging (approval)
  → deploy-production pulls :latest into cicd-demo-production (approval)
```

Without Render credentials, deploy jobs still succeed and *simulate* promotion
so you can learn the Actions graph first.
