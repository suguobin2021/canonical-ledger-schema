# Contributing

Thanks for considering a contribution.

## Good starting points

Open issues labeled `good first issue` are intentionally scoped for a first contribution. Issues labeled `help wanted` are also open to community implementation.

Before coding, leave a short comment on the issue describing the approach you plan to take. This helps avoid duplicate work.

## Development

1. Fork the repository and create a focused branch.
2. Keep changes strategy-agnostic and use synthetic fixtures only.
3. Do not add proprietary datasets, private trading logic, credentials, or real account data.
4. Install locally with `python -m pip install .`.
5. Run `python -m unittest discover -s tests -v`.
6. Open a pull request that links the issue and explains the behavioral change.

Pull requests should stay small enough to review, include regression tests for changed behavior, and keep Python 3.10, 3.11, and 3.12 CI green.
