# Dragen utils

![test](https://github.com/UMCUGenetics/dragen_utils/actions/workflows/test.yml/badge.svg)
![lint](https://github.com/UMCUGenetics/dragen_utils/actions/workflows/lint.yml/badge.svg)

Utility commands for nextflow pipelines using Illumina Dragen, bundled as a single installable package.

## Commands

| Command                   | Description                                                            | NF module                                                                                                                        |
| ------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `dragen-utils fastq_list` | Generate csv file which can be used as input for Dragen --fastq-list   | [dragenutils/fastqlist](https://github.com/UMCUGenetics/NF-Modules/tree/main/modules/UMCUGenetics/dragenutils/fastqlist/main.nf) |
| `dragen-utils dx_qc`      | Generate csv file with QC statistics relevant for diagnostic sample QC | [dragenutils/dxqc](https://github.com/UMCUGenetics/NF-Modules/tree/main/modules/UMCUGenetics/dragenutils/dxqc/main.nf)           |

## Container image

Each release publishes a multi-arch image to `ghcr.io/umcugenetics/dragen-utils:<version>`, built from `uv.lock` so the dependency set is exactly
the one the tests ran against. This is what the `dragenutils` Nextflow modules pin their `container` directive to.

```sh
docker run ghcr.io/umcugenetics/dragen-utils:1.0.0 dragen-utils --version
```

Singularity pulls the same image directly:

```sh
singularity exec docker://ghcr.io/umcugenetics/prs-utils:1.0.0 dragen-utils --version
```

Build it locally without publishing:

```sh
docker build -t dragen-utils:dev .
```

## Development

Setup and run the test suite:

```sh
uv sync
uv run pytest tests
```

Linting and formatting use [Ruff](https://docs.astral.sh/ruff/):

```sh
uv run ruff check src tests
uv run ruff format src tests
```

### GitHub Actions

This repository contains two GitHub actions workflows (`.github/workflos/`): `lint.yml` and `test.yml`. The lint workflow uses the [ruff-action](https://github.com/astral-sh/ruff-action) action to run ruff. The test workflow uses the [setup-uv action](https://github.com/astral-sh/setup-uv) to setup uv, install dependencies and run tests. Both actions are configured to run on each pull request and push to main and develop.

### pre-commit

Git pre-commit hooks enable you to run certain commands before each commit and can be used to check code style before committing. The file `.pre-commit-config.yaml` contains the [Ruff](https://docs.astral.sh/ruff/) [pre-commit](https://pre-commit.com) hook, which will automatically run Ruff before each commit. Run the following command to install the git commit hook: `uvx pre-commit install`.
