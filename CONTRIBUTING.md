# Contributing

Keep both production files self-contained so RFPro's
`empro.toolkit.scripting.run()` can load either one by path. Do not add PySide6
or `empro` as PyPI dependencies; they must come from the target Keysight
installation.

Before committing, run:

```bash
python -m py_compile rfpro_scripts/*.py scripts/*.py
python -m unittest discover -s tests -v
```

Any change to public RFPro/EMPro calls must be rechecked against the installed
release's Python documentation and examples. A local static test is not a
substitute for running both scripts inside RFPro with a small completed sweep.
