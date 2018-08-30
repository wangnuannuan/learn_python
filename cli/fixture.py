"""Test fixtures and decorators that are not test specific"""

import functools
import gc
import inspect
import logging
import pprint
import unittest
import weakref
import time
# time granted to asyncio to receive datagrams sent via loopback, and to close
# connections. if tearDown checks fail erratically, tune this up -- but it
# causes per-fixture delays.
CLEANUPTIME = 0.01

ASYNCTEST_TIMEOUT = 3 * 60

def test_is_successful(testcase):
    return not any(e[1] is not None for e in testcase._outcome.errors)



class WithLogMonitoring(unittest.TestCase):
    def setUp(self):
        self.handler = self.ListHandler()

        logging.root.setLevel(0)
        logging.root.addHandler(self.handler)

        super(WithLogMonitoring, self).setUp()

    def tearDown(self):
        super(WithLogMonitoring, self).tearDown()

        logging.root.removeHandler(self.handler)

        formatter = logging.Formatter(fmt='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        self.assertTrue(test_is_successful(self), "Previous errors were raised."
                " Complete log:\n" + "\n".join(
                formatter.format(x) for x in self.handler if x.name != 'asyncio'),
                )

    class ListHandler(logging.Handler, list):
        def emit(self, record):
            self.append(record)

    def assertWarned(self, message):
        """Assert that there was a warning with the given message.

        This function also removes the warning from the log, so an enclosing
        @no_warnings (or @precise_warnings) can succed."""
        for entry in self.handler:
            if entry.msg == message and entry.levelno == logging.WARNING:
                self.handler.remove(entry)
                break
        else:
            raise AssertionError("Warning not logged: %r"%message)


class Destructing(WithLogMonitoring):
    def _del_to_be_sure(self, attribute):
        weaksurvivor = weakref.ref(getattr(self, attribute))
        delattr(self, attribute)
        # let everything that gets async-triggered by close() happen
        time.sleep(CLEANUPTIME)
        gc.collect()

        def snapshot():
            canary = object()
            survivor = weaksurvivor()
            if survivor is None:
                return None

            all_referrers = gc.get_referrers(survivor)
            canary_referrers = gc.get_referrers(canary)
            referrers = [r for r in all_referrers if r not in canary_referrers]
            assert len(all_referrers) == len(referrers) + 1, "Canary to filter out the debugging tool's reference did not work"

            def _format_frame(frame, survivor_id):
                return "%s as %s in %s" % (
                    frame,
                    " / ".join(k for (k, v) in frame.f_locals.items() if id(v) == survivor_id),
                    frame.f_code)

            # can't use survivor in list comprehension, or it would be moved
            # into a builtins.cell rather than a frame, and that won't spew out
            # the details _format_frame can extract
            survivor_id = id(survivor)
            referrer_strings = [
                    _format_frame(x, survivor_id) if str(type(x)) == "<class 'frame'>" else pprint.pformat(x) for x in
                    referrers]
            formatted_survivor = pprint.pformat(vars(survivor))
            return "Survivor found: %r\nReferrers of the survivor:\n*"\
                   " %s\n\nSurvivor properties: %s" % (
                       survivor, "\n* ".join(referrer_strings),formatted_survivor)

        s = snapshot()

        #if not test_is_successful(self):
            # An error was already logged, and that error's backtrace usually
            # creates references that make any attempt to detect lingering
            # references fuitile. It'll show an error anyway, no use in
            # polluting the logs.
            #return

        if s is not None:
            original_s = s
            if False: # enable this if you think that a longer timeout would help
                # this helped finding that timer cancellations don't free the
                # callback, but in general, expect to modify this code if you
                # have to read it; this will need adjustment to your current
                # debugging situation
                logging.root.info("Starting extended grace period")
                for i in range(10):
                    time.sleep(1)
                    gc.collect()
                    s = snapshot()
                    if s is None:
                        logging.root.info("Survivor vanished after %r iterations" % i+1)
                        break
                snapshotsmessage = "Before extended grace period:\n" + original_s + "\n\nAfter extended grace period:\n" + ("the same" if s == original_s else s)
            else:
                snapshotsmessage = s
            errormessage = "Protocol %s was not garbage collected.\n\n"%attribute + snapshotsmessage
            self.fail(errormessage)