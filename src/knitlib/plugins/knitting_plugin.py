# -*- coding: utf-8 -*-
#    This file is part of Knitlib, based on AYAB.
#    Copyright 2014, 2015 Sebastian Oliva
#    https://github.com/fashiontec/knitlib/

import logging
from fysom import Fysom


class BaseKnittingPlugin(Fysom):
    """A generic plugin implementing a state machine for knitting.

    Subclasses inherit the basic State Machine defined in __init__.
    """

    def onknit(self, e):
        """Callback when state machine executes knit().

        Starts the knitting process, this is the only function call that can block indefinitely, as it is called from an instance
        of an individual Thread, allowing for processes that require timing and/or blocking behaviour.
        """
        raise NotImplementedError(
            self.__NOT_IMPLEMENTED_ERROR.format("onknit. It is used for the main 'knitting loop'."))

    def onfinish(self, e):
        """Callback when state machine executes finish().

        When finish() gets called, the plugin is expected to be able to restore it's state back when configure() gets called.
        Finish should trigger a Process Completed notification so the user can operate accordingly.
        """
        raise NotImplementedError(
            self.__NOT_IMPLEMENTED_ERROR.format("onfinish. It is a callback that is called when knitting is over."))

    def onconfigure(self, e):
        """Callback when state machine executes configure(options={})

        This state gets called to configure the plugin for knitting. It can either
        be called when first configuring the plugin, when an error happened and a
        reset is necessary.

        Args:
          options: An object holding an options dict.
        """
        raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format(
            "onconfigure. It is used to configure the knitting plugin before starting."))

    def publish_options(self):
        raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format(
            "publish_options must be defined. It is used to expose the possible knitting options."))

    def validate_configuration(self, conf):
        raise NotImplementedError(self.__NOT_IMPLEMENTED_ERROR.format(
            "validate_configuration must be defined. It verifies configurations are valid."))

    def register_interactive_callbacks(self, callbacks=None):
        """Serves to register a dict of callbacks that require interaction by the User,

         Interactive callbacks serve to block operation until a human acts on them. Interactive callbacks can include
         physical operations (set needles, move knob, flip switch), decisions (yes/no or cancel), or simply human
         acknowledgement.

         Args:
            callbacks: keys can be info, warning, progress, error.

         """
        if callbacks is None:
            callbacks = {}
        self.interactive_callbacks = callbacks

    def __interactive_info(message):
        logging.info(message)
        raw_input()

    def __interactive_warn(message):
        logging.info(message)
        raw_input()

    def __interactive_error(message):
        logging.error(message)
        raw_input()

    def __log_progress(message):
        logging.info(message)

    def __init__(self, callbacks_dict=None, interactive_callbacks=None):
        self.__NOT_IMPLEMENTED_ERROR = "Classes that inherit from KnittingPlugin should implment {0}"
        self.interactive_callbacks = {}

        if interactive_callbacks is None:
            self.register_interactive_callbacks({
                "info": BaseKnittingPlugin.__interactive_info,
                "user_action": BaseKnittingPlugin.__interactive_info,
                "warning": BaseKnittingPlugin.__interactive_warn,
                "error": BaseKnittingPlugin.__interactive_error,
                "progress": BaseKnittingPlugin.__log_progress
            })
        else:
            self.register_interactive_callbacks(interactive_callbacks)

        if callbacks_dict is None:
            callbacks_dict = {
                'onknit': self.onknit,
                'onconfigure': self.onconfigure,
                'onfinish': self.onfinish,
            }
        Fysom.__init__(self, {
            'initial': 'activated',
            'events': [  # TODO: add more states for handling error management.
                         {'name': 'configure', 'src': 'activated', 'dst': 'configured'},
                         {'name': 'configure', 'src': 'configured', 'dst': 'configured'},
                         {'name': 'configure', 'src': 'finished', 'dst': 'configured'},
                         {'name': 'configure', 'src': 'error', 'dst': 'configured'},
                         {'name': 'knit', 'src': 'configured', 'dst': 'knitting'},
                         {'name': 'finish', 'src': 'knitting', 'dst': 'finished'},
                         {'name': 'fail', 'src': 'knitting', 'dst': 'error'}],
            'callbacks': callbacks_dict
        })
