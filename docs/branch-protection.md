# Copy this into GitHub → Settings → Branches → Add rule for `main`
# (GitHub API / UI required — branch protection cannot live in the repo alone.)

# Recommended rules for this demo:
#   ✓ Require a pull request before merging
#   ✓ Require status checks to pass before merging:
#       - lint
#       - unit-tests
#       - coverage
#       - integration-tests
#       - build-image
#   ✓ Require branches to be up to date before merging
#   ✓ Do not allow bypassing the above settings
#   ✓ Restrict who can push to matching branches (optional)

# After the first successful Actions run, the check names above appear
# in the branch-protection UI under "Status checks that are required."
