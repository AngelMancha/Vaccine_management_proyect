#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.pycharm")


name = "GE3_2022"
default_task = "publish"

description ="",
long_description = "",
long_description_content_type = "text/markdown"


@init
def set_properties(project):
    pass
