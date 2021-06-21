# Flask Web Framework

The goal of this project is to create a lightweight collaboration framework. For this, it is based on Flask.

## Directory Structure

```
o
|-- configs/
|-- datasets/
|-- executes/
|-- middlewares/
|-- mls/
|-- models/
|-- modules/
|-- packages/
|-- routes/
|-- schedules/
|-- static/
|   `-- none/
|       |-- includes/
|       |-- assets/
|       |-- downloads/
|       |-- uploads/
|       `-- vendor/
|-- templates/
|   `-- none/
|       |-- htmls/
|       |-- includes/
|       |-- layouts/
|       |-- macros/
|       |-- 404.jinja
|       `-- index.jinja
|-- users/
|   `-- anonymous/
`-- app.py
```

## Dataset

The datasets directory is a collection of data.

## Execute

The executes directory is a collection of files that are executed in subprocesses.

**Run the script file in the executes directory.**

```python
from modules.flask import subprocess_exec
subprocess_exec('execute.py')
```

**Run all script files in the executes directory.**

```python
from modules.flask import subprocess_execs
subprocess_execs()
```

## Middleware

The mls directory is a collection of decorators.

## ML

The mls directory is a collection of machine learning models.

## Model

If a file with the same name as the routing file exists in the model directory, it is dynamically imported and assigned to the model variable.

```python
model = import_model(filename)
```

If you have multiple routes in your routing file, you can use a parameter to change the name of the file to import.

```python
model = import_model(filename, suffix='')
```

## Module

The bins directory is a collection of functions used globally.

## Package

The bins directory is a collection of package.

## Route

File names in the path directory are converted to URL slugs. Double underscores are used as URL slug separators, and single underscores are converted to hyphens.

If the filename starts with an underscore, it is not rendered.

```python
dirname__dir_name to /dirname/dir-name/
```

To exclude rendering, add the name of the file you want to exclude to the auto_register_blueprint function in app.py.

```python
auto_register_blueprint(excludes=['filename'])
```

## Schedule

The schedules directory is a collection of files that run periodically.

**app.py**

```python
from schedules.schedule import job1, job2
scheduler.add_job(func=job1, trigger="interval", id='do_job1', seconds=3)
scheduler.add_job(func=job2, trigger="cron", id='do_job2', hour='5', minute='0')
```

**schedule.py**

```python
def job1():
    pass
def job2():
    pass
```

## Template

**Render**  
If there is a file with the same name in the same directory, the file extensions are rendered in the order of html, jinja, and jinja2.

**Inc**  
A collection of files used globally within a template.

**Layout**  
The page layout can be set in the routing file. The supported layouts are content, sidebar-content, content-sidebar, and sidebar-content-sidebar.

## License

This software is licensed under the MIT license.
