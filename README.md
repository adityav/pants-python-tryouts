# pants python tryout

Repo to tryout pants for data engineering projects

## Current Issue

Using a constraints file causes `ModuleNotFoundError: No module named 'pyarrow'` when running tests.

Without constraints file, hellospark_test works correctly.
```
➜ ./pants test helloworld/sparkjob/hellospark_test.py
19:14:59.81 [INFO] Completed: Building 4 requirements for requirements.pex from the python-default.lock resolve: pandas==1.5.1, pyarrow==6.0.1, pyspark[sql]==3.3.1, pytest==6.2.5
19:15:01.36 [INFO] Completed: Building pytest_runner.pex
19:15:11.84 [INFO] Completed: Run Pytest - helloworld/sparkjob/hellospark_test.py:tests succeeded.

✓ helloworld/sparkjob/hellospark_test.py:tests succeeded in 10.35s.
```
On adding a constraints file in `pants.toml`:

```
[python.resolves_to_constraints_file]
python-default = "constraints-3.10.txt"
```

Getting error:

```
➜ ./pants generate-lockfiles                          
19:17:41.08 [INFO] Initializing scheduler...
19:17:41.40 [INFO] Scheduler initialized.
19:18:01.38 [INFO] Completed: Generate lockfile for python-default
19:18:01.39 [INFO] Wrote lockfile for the resolve `python-default` to python-default.lock
./pants test helloworld/sparkjob/hellospark_test.py
19:19:25.82 [ERROR] Completed: Run Pytest - helloworld/sparkjob/hellospark_test.py:tests failed (exit code 2).
============================= test session starts ==============================
platform darwin -- Python 3.10.9, pytest-7.0.1, pluggy-1.0.0
rootdir: /private/var/folders/0t/dmh8ynt13pbc2y2stvb0by6c0000gn/T/pants-sandbox-aA4jsU
plugins: xdist-2.5.0, forked-1.4.0, cov-3.0.0
collected 0 items / 1 error

==================================== ERRORS ====================================
___________ ERROR collecting helloworld/sparkjob/hellospark_test.py ____________
ImportError while importing test module '/private/var/folders/0t/dmh8ynt13pbc2y2stvb0by6c0000gn/T/pants-sandbox-aA4jsU/helloworld/sparkjob/hellospark_test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/local/Cellar/python@3.10/3.10.9/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
helloworld/sparkjob/hellospark_test.py:1: in <module>
    from helloworld.sparkjob import hellospark
helloworld/sparkjob/hellospark.py:5: in <module>
    import pyarrow as pa
E   ModuleNotFoundError: No module named 'pyarrow'
- generated xml file: /private/var/folders/0t/dmh8ynt13pbc2y2stvb0by6c0000gn/T/pants-sandbox-aA4jsU/helloworld.sparkjob.hellospark_test.py.tests.xml -
=========================== short test summary info ============================
ERROR helloworld/sparkjob/hellospark_test.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.82s ===============================



✕ helloworld/sparkjob/hellospark_test.py:tests failed in 1.65s.
```


## past issues
### Unable to run a spark job

on running:
```
./pants run helloworld/sparkjob/hellospark.py
```
, getting error:

`ModuleNotFoundError: No module named 'pandas'`

`requirements.txt` contains dependency `pyspark[pandas_on_spark]==3.3.1` which has `pandas` and `pyarrow` as extra dependencies.

#### soln
There are 2 solns:

1. Run using a `pex_binary` target, like this:
```
pex_binary(
    name="main",
    entry_point="hellospark.py",
    execution_mode="venv"
)
```
Thanks to @jsirois for his PR: https://github.com/adityav/pants-python-tryouts/pull/1
From him, on slack:
> When you need maximum compatibility or any form of control, running a python_sourcesowned file is not what you want. That must necessarily choose one set of options for all runs. Here the option you needed was to tell Pants to tell Pex to use a venv (See: https://www.pantsbuild.org/docs/reference-pex_binary#codeexecution_modecode) https://github.com/adityav/pants-python-tryouts/pull/1

2. Darcy Shen in slack suggested adding env vars like [here](https://github.com/da-tubi/jupyter-notebook-best-practice/blob/26bbbe0919b8753550634205a4d97c84c2a80729/notebooks/helper.py#L6-L7)

```
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
```

---
# templated Readme below

# example-python
An example repository to demonstrate Python support in Pants.

See [pantsbuild.org](https://www.pantsbuild.org/docs) for much more detailed documentation.

This is only one possible way of laying out your project with Pants. See 
[pantsbuild.org/docs/source-roots#examples](https://www.pantsbuild.org/docs/source-roots#examples) for some other
example layouts.

# Running Pants

You run Pants goals using the `./pants` wrapper script, which will bootstrap the
configured version of Pants if necessary.

> :question: Running with Apple Silicon and/or MacOS? You will want to make changes to the `search_path` and
`interpreter_constraints` values in `pants.toml` before running `./pants` - there is guidance in `pants.toml`
for those settings.

Use `./pants --version` to see the version of Pants configured for the repo (which you can also find
in `pants.toml`).

# Goals

Pants commands are called _goals_. You can get a list of goals with

```
./pants help goals
```

# Targets

Targets are a way of setting metadata for some part of your code, such as timeouts for tests and 
entry points for binaries. Targets have types like `python_source`, `resources`, and 
`pex_binary`. They are defined in `BUILD` files.

Pants goals can be invoked on targets or directly on source files (which is often more intuitive and convenient).
In the latter case, Pants locates target metadata for the source files as needed.

## File specifications

Invoking goals on files is straightforward, e.g.,

```
./pants test helloworld/greet/greeting_test.py
```

You can use globs:

```
./pants lint helloworld/greet/*.py
```

But note that these will be expanded by your shell, so this is equivalent to having used

```
./pants lint helloworld/greet/__init__.py helloworld/greet/greeting.py helloworld/greet/greeting_test.py
```

If you want Pants itself to expand the globs (which is sometimes necessary), you must quote them in the shell:

```
./pants lint 'helloworld/greet/*.py'
```

You can run on all changed files:

```
./pants --changed-since=HEAD lint
```

You can run on all changed files, and any of their "dependees":

```
./pants --changed-since=HEAD --changed-dependees=transitive test
```

## Target specifications

Targets are referenced on the command line using their address, of the form `path/to/dir:name`, e.g.,

```
./pants lint helloworld/greet:lib
```

You can glob over all targets in a directory with a single trailing `:`, or over all targets in a directory
and all its subdirectories with a double trailing `::`, e.g.,

```
./pants lint helloworld::
```

## Globbing semantics

When you glob over files or targets, Pants knows to ignore ones that aren't relevant to the requested goal.
For example, if you run the `test` goal over a set of files that includes non-test files, Pants will just ignore
those, rather than error. So you can safely do things like

```
./pants test ::
```

To run all tests.

# Example Goals

Try these out in this repo!

## List targets

```
./pants list ::  # All targets.
./pants list 'helloworld/**/*.py'  # Just targets containing Python code.
```

## Run linters and formatters

```
./pants lint ::
./pants fmt helloworld/greet::
```

## Run MyPy

```
./pants check ::
```

## Run tests

```
./pants test ::  # Run all tests in the repo.
./pants test --output=all ::  # Run all tests in the repo and view pytest output even for tests that passed (you can set this permanently in pants.toml).
./pants test helloworld/translator:tests  # Run all the tests in this target.
./pants test helloworld/translator/translator_test.py  # Run just the tests in this file.
./pants test helloworld/translator/translator_test.py -- -k test_unknown_phrase  # Run just this one test by passing through pytest args.
```

## Create a PEX binary

```
./pants package helloworld/main.py
```

## Run a binary directly

```
./pants run helloworld/main.py
```

## Open a REPL

```
./pants repl helloworld/greet:lib  # The REPL will have all relevant code and dependencies on its sys.path.
./pants repl --shell=ipython helloworld/greet:lib --no-pantsd  # To use IPython, you must disable Pantsd for now.
```

## Build a wheel / generate `setup.py`

This will build both a `.whl` bdist and a `.tar.gz` sdist.

```
./pants package helloworld/translator:dist
```

## Count lines of code

```
./pants count-loc '**/*'
```
## Create virtualenv for IDE integration

```
./pants export ::
```
