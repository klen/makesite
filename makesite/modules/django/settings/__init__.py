from os import path as op


SOURCE_DIR = op.abspath(op.dirname(op.dirname(__file__)))
PROJECT_DIR = op.dirname(SOURCE_DIR)
PROJECT_NAME = "%s.%s" % (op.basename(op.dirname(PROJECT_DIR)), op.basename(PROJECT_DIR))
