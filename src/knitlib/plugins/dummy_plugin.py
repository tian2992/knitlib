# -*- coding: utf-8 -*-
import logging
import time
import knitting_plugin


class DummyKnittingPlugin(knitting_plugin.BaseKnittingPlugin):
  """Implements a sample knitting plugin that allows for simple operation emulation."""

  def __init__(self):
    super(DummyKnittingPlugin, self).__init__()
    self.register_interactive_callbacks()

  base_log_string = "{} has been called on dummy knitting plugin."

  def onknit(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onknit"))
    # In order to simulate blocking we make it sleep.
    for i in range(5):
      time.sleep(1)
      print("Knitted line: {}".format(i))

  def onfinish(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onfinish"))

  def onconfigure(self, e):
    logging.debug(DummyKnittingPlugin.base_log_string.format("onconfigure"))

  def publish_options(self):
    logging.debug(DummyKnittingPlugin.base_log_string.format("pub options"))
