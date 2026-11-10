# Releasing Aether on npm

The npm package is a CLI and a set of local skills and agent entries. It has no JavaScript import API. Node.js 18 or newer is supported for installation. The graph renderer requires Python 3.10 or newer and Git. The kit's own validators and tests require Python 3.10 or newer and use the standard library only.

Versions follow SemVer. Before 1.0, increment the minor version for a breaking installer or skill change and the patch version for compatible fixes. Note breaking changes and upgrade steps in `CHANGELOG.md`.

1. Update `package.json`, the pinned `npx` command in `README.md`, and `CHANGELOG.md` to the same version.
2. Run `npm test`, `python scripts/validate_agent_kit.py`, `python scripts/validate_evals.py`, `python -m unittest discover -s scripts -p 'test_*.py'`, and `npm pack --dry-run --json`. Review the complete file list before release.
3. Commit and push the release on `main`. Create and publish a GitHub release tagged `v` followed by the package version. `.github/workflows/publish-npm.yml` checks the tag, tests the tagged commit, packs once, and publishes that tarball with provenance.
4. Verify the exact version from the npm registry in a clean directory and confirm the package's `latest` tag and provenance.

The first publish uses a short-lived granular npm token stored only as the GitHub Actions repository secret `NPM_TOKEN`. After the package exists, configure an npm trusted publisher for GitHub user `theshantanujoshi`, repository `aether`, and workflow `publish-npm.yml`; allow direct publishing. Then remove `NODE_AUTH_TOKEN` from the workflow and delete `NPM_TOKEN` from GitHub. Trusted publishing requires a compatible npm CLI and Node version on the runner; the workflow uses Node 24. Review npm's current trusted publishing instructions before that change.
