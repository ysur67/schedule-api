from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType

from celery import Celery

import celery_app.tasks


def has_init_tasks_method(module: ModuleType) -> bool:
    return hasattr(module, "init_tasks") and callable(module.init_tasks)


def init_tasks(app: Celery):
    package = celery_app.tasks
    prefix = package.__name__ + "."
    for _, name, _ in iter_modules(package.__path__, prefix):
        module = import_module(name)
        if has_init_tasks_method(module):
            module.init_tasks(app)
