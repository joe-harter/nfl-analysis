
## Set Up

Create a virtual environment. It's easiest to use Miniconda to manage Python and dependencies.

You can follow the instruction [here](https://docs.conda.io/projects/miniconda/en/latest/index.html#quick-command-line-install) to download and install Miniconda on your machine.

This project uses Python 3.10. Create an environment with

```bash
conda create -n nflverse-analysis python=3.10
```

Activate the virtual environment with

```bash
conda activate nflverse-analysis
```

Install all python dependencies

```
pip install -r requirements.txt
```