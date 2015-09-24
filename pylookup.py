#!/usr/bin/python3

"""Display the pylint message id for a given message name"""

import argparse
import logging
import random
import os
import subprocess
import sys

__program__ = 'pylookup'
__description__ = 'Display the pylint message id for a given message name.'


# pylint --list-msgs 2>/dev/null | awk -F '[()]' $'BEGIN{ OFS=":" } /^:/ { match($1, /^:(.+) /, a); msg=a[1]; id=$2; printf "    \'%s\': \'%s\',\\n", msg, id }' | sort | sed '$ s/,$//'
MSGLIST = {
    'abstract-class-instantiated': 'E0110',
    'abstract-class-little-used': 'R0922',
    'abstract-class-not-used': 'R0921',
    'abstract-method': 'W0223',
    'access-member-before-definition': 'E0203',
    'anomalous-backslash-in-string': 'W1401',
    'anomalous-unicode-escape-in-string': 'W1402',
    'arguments-differ': 'W0221',
    'assert-on-tuple': 'W0199',
    'assigning-non-slot': 'E0237',
    'assignment-from-none': 'W1111',
    'assignment-from-no-return': 'E1111',
    'astroid-error': 'F0002',
    'attribute-defined-outside-init': 'W0201',
    'bad-builtin': 'W0141',
    'bad-classmethod-argument': 'C0202',
    'bad-context-manager': 'E0235',
    'bad-continuation': 'C0330',
    'bad-exception-context': 'E0703',
    'bad-except-order': 'E0701',
    'bad-format-character': 'E1300',
    'bad-format-string-key': 'W1300',
    'bad-format-string': 'W1302',
    'bad-indentation': 'W0311',
    'bad-inline-option': 'I0010',
    'bad-mcs-classmethod-argument': 'C0204',
    'bad-mcs-method-argument': 'C0203',
    'bad-open-mode': 'W1501',
    'bad-option-value': 'E0012',
    'bad-reversed-sequence': 'E0111',
    'bad-staticmethod-argument': 'W0211',
    'bad-str-strip-call': 'E1310',
    'bad-super-call': 'E1003',
    'bad-whitespace': 'C0326',
    'bare-except': 'W0702',
    'binary-op-exception': 'W0711',
    'blacklisted-name': 'C0102',
    'boolean-datetime': 'W1502',
    'broad-except': 'W0703',
    'catching-non-exception': 'E0712',
    'cell-var-from-loop': 'W0640',
    'cyclic-import': 'R0401',
    'dangerous-default-value': 'W0102',
    'deprecated-module': 'W0402',
    'deprecated-pragma': 'I0022',
    'duplicate-argument-name': 'E0108',
    'duplicate-code': 'R0801',
    'duplicate-key': 'W0109',
    'empty-docstring': 'C0112',
    'eval-used': 'W0123',
    'exec-used': 'W0122',
    'expression-not-assigned': 'W0106',
    'fatal': 'F0001',
    'file-ignored': 'I0013',
    'fixme': 'W0511',
    'format-combined-specification': 'W1305',
    'format-needs-mapping': 'E1303',
    'function-redefined': 'E0102',
    'global-at-module-level': 'W0604',
    'global-statement': 'W0603',
    'global-variable-not-assigned': 'W0602',
    'global-variable-undefined': 'W0601',
    'ignored-builtin-module': 'F0003',
    'import-error': 'F0401',
    'import-self': 'W0406',
    'inherit-non-class': 'E0239',
    'init-is-generator': 'E0100',
    'interface-is-not-class': 'E0221',
    'interface-not-implemented': 'R0923',
    'invalid-all-object': 'E0604',
    'invalid-format-index': 'W1307',
    'invalid-name': 'C0103',
    'invalid-sequence-index': 'E1126',
    'invalid-slice-index': 'E1127',
    'invalid-slots': 'E0238',
    'invalid-slots-object': 'E0236',
    'line-too-long': 'C0301',
    'locally-disabled': 'I0011',
    'locally-enabled': 'I0012',
    'logging-format-interpolation': 'W1202',
    'logging-format-truncated': 'E1201',
    'logging-not-lazy': 'W1201',
    'logging-too-few-args': 'E1206',
    'logging-too-many-args': 'E1205',
    'logging-unsupported-format': 'E1200',
    'lost-exception': 'W0150',
    'method-check-failed': 'F0202',
    'method-hidden': 'E0202',
    'missing-docstring': 'C0111',
    'missing-final-newline': 'C0304',
    'missing-format-argument-key': 'W1303',
    'missing-format-attribute': 'W1306',
    'missing-format-string-key': 'E1304',
    'missing-interface-method': 'E0222',
    'missing-kwoa': 'E1125',
    'missing-module-attribute': 'C0121',
    'missing-reversed-argument': 'E0109',
    'mixed-format-string': 'E1302',
    'mixed-indentation': 'W0312',
    'mixed-line-endings': 'C0327',
    'multiple-statements': 'C0321',
    'no-init': 'W0232',
    'no-member': 'E1101',
    'no-method-argument': 'E0211',
    'no-name-in-module': 'E0611',
    'nonexistent-operator': 'E0107',
    'non-iterator-returned': 'W0234',
    'non-parent-init-called': 'W0233',
    'no-self-argument': 'E0213',
    'no-self-use': 'R0201',
    'not-callable': 'E1102',
    'notimplemented-raised': 'E0711',
    'not-in-loop': 'E0103',
    'no-value-for-parameter': 'E1120',
    'parse-error': 'F0010',
    'pointless-except': 'W0704',
    'pointless-statement': 'W0104',
    'pointless-string-statement': 'W0105',
    'protected-access': 'W0212',
    'raising-bad-type': 'E0702',
    'raising-non-exception': 'E0710',
    'raw-checker-failed': 'I0001',
    'redefined-builtin': 'W0622',
    'redefined-outer-name': 'W0621',
    'redefine-in-handler': 'W0623',
    'redundant-keyword-arg': 'E1124',
    'redundant-unittest-assert': 'W1503',
    'reimported': 'W0404',
    'return-in-init': 'E0101',
    'return-outside-function': 'E0104',
    'signature-differs': 'W0222',
    'star-args': 'W0142',
    'superfluous-parens': 'C0325',
    'super-init-not-called': 'W0231',
    'suppressed-message': 'I0020',
    'syntax-error': 'E0001',
    'too-few-format-args': 'E1306',
    'too-few-public-methods': 'R0903',
    'too-many-ancestors': 'R0901',
    'too-many-arguments': 'R0913',
    'too-many-branches': 'R0912',
    'too-many-format-args': 'E1305',
    'too-many-function-args': 'E1121',
    'too-many-instance-attributes': 'R0902',
    'too-many-lines': 'C0302',
    'too-many-locals': 'R0914',
    'too-many-public-methods': 'R0904',
    'too-many-return-statements': 'R0911',
    'too-many-statements': 'R0915',
    'trailing-whitespace': 'C0303',
    'truncated-format-string': 'E1301',
    'unbalanced-tuple-unpacking': 'W0632',
    'undefined-all-variable': 'E0603',
    'undefined-loop-variable': 'W0631',
    'undefined-variable': 'E0602',
    'unexpected-keyword-arg': 'E1123',
    'unexpected-line-ending-format': 'C0328',
    'unnecessary-lambda': 'W0108',
    'unnecessary-pass': 'W0107',
    'unnecessary-semicolon': 'W0301',
    'unpacking-non-sequence': 'W0633',
    'unreachable': 'W0101',
    'unrecognized-inline-option': 'E0011',
    'unresolved-interface': 'F0220',
    'unused-argument': 'W0613',
    'unused-format-string-argument': 'W1304',
    'unused-format-string-key': 'W1301',
    'unused-import': 'W0611',
    'unused-variable': 'W0612',
    'unused-wildcard-import': 'W0614',
    'used-before-assignment': 'E0601',
    'useless-else-on-loop': 'W0120',
    'useless-suppression': 'I0021',
    'wildcard-import': 'W0401',
    'wrong-spelling-in-comment': 'C0401',
    'wrong-spelling-in-docstring': 'C0402',
    'yield-outside-function': 'E0105'
}


class RebuildAction(argparse.Action):

    """argparse action to rebuild script's message list."""

    def __call__(self, parser, args, values, option_string=None):
        setattr(args, self.dest, values)
        RebuildClass()


class RebuildClass:

    """Rebuild script's message list."""

    def __init__(self):
        # generate a random backup file extension
        self.bak = '.bak' + str(random.random())[-4:]
        self.data = None
        self.replacement = None

        self.check()
        self.prepare()

        original_perms = os.stat(__file__).st_mode

        try:
            self.backup()
            self.writetofile()
            assert os.path.isfile(__file__) and os.path.getsize(__file__) > 0

        except:  # pylint: disable=W0702
            self.exception()
            sys.exit(1)

        self.finish()

        current_perms = os.stat(__file__).st_mode

        fatalities = []

        try:
            assert original_perms == current_perms
        except AssertionError:
            fatalities.append("Failed to restore permissions for '%s'" % __file__)

        try:
            assert not os.path.isfile(__file__ + self.bak)
        except AssertionError:
            fatalities.append("Failed to remove backup file '%s' after rebuild" % __file__ + self.bak)

        if fatalities:
            for msg in fatalities:
                logging.error(msg)
            sys.exit(1)

        sys.exit(0)

    def backup(self):
        """Move/rename file to backup."""
        move(__file__, __file__ + self.bak)

        if not os.path.isfile(__file__ + self.bak):
            logging.fatal("Unable to create backup file '%s' prior to rebuild", __file__ + self.bak)
            sys.exit(1)
        elif os.path.isfile(__file__):
            logging.fatal("Unable to move '%s' prior to rebuild", __file__)
            sys.exit(1)

    def check(self):
        """Check whether a rebuild is necessary."""

        command = """pylint --list-msgs 2>/dev/null | awk -F '[()]' 'BEGIN{ OFS=":" } /^:/ { match($1, /^:(.+) /, a); msg=a[1]; id=$2; printf "    .%s.: .%s.,\\n", msg, id }' | sort | tr . \\' | sed '$ s/,//'"""

        self.data = subprocess.check_output(command,
                                            executable='bash',
                                            shell=True,
                                            stderr=subprocess.PIPE).decode()

        if not self.data:
            logging.fatal('Unable to acquire messages necessary to rebuild')
            sys.exit(1)

        exec('NEW_MSGLIST = {%s}' % self.data, globals())

        if MSGLIST == NEW_MSGLIST:
            logging.info('Already up to date')
            sys.exit(0)

        logging.info('Rebuilding list now')

    def exception(self):
        """Restore files to their original state in the event of an exception."""

        logging.error("Rebuild of '%s' failed...", __file__)

        # check if backup exists and restore it if so
        if os.path.isfile(__file__ + self.bak):
            if os.path.isfile(__file__):
                remove(__file__)
            move(__file__ + self.bak, __file__)

    def finish(self):
        # set permissions using backup as a reference
        chmod(__file__, __file__ + self.bak)

        # remove the backup
        remove(__file__ + self.bak)

    def prepare(self):
        import re
        pattern = re.compile(r'^MSGLIST = {[^{^]*}', re.MULTILINE)

        with open(__file__, 'rU') as fileobj:
            original = fileobj.read()
            self.replacement = pattern.sub('MSGLIST = {\n%s}' % self.data, original)

        if self.replacement == original:
            logging.fatal("Rebuild failed... '%s' may be damaged", __file__)
            sys.exit(1)

    def writetofile(self):
        from tempfile import NamedTemporaryFile

        try:
            # create a temp file
            tf = NamedTemporaryFile()

            # write data to temp file
            tf.write(self.replacement.encode())

            # ensure all data is written to temp file
            tf.flush()

            # write data to file
            writer(tf.name, __file__)

        finally:
            tf.close()


def chmod(path, reference):
    """Set file permissions."""
    execute("chmod --reference='{1}' '{0}' &>/dev/null || sudo chmod --reference='{1}' '{0}' &>/dev/null".format(path, reference))


def execute(command):
    """Execute command."""
    subprocess.check_output(command, executable='bash', shell=True)


def move(origin, destination):
    """Move file."""
    execute("mv '{0}' '{1}' &>/dev/null || sudo mv '{0}' '{1}' &>/dev/null".format(origin, destination))


# def rebuild():
#     import os
#     import re
#     import tempfile
#     import subprocess

#     command = """pylint --list-msgs 2>/dev/null | awk -F '[()]' 'BEGIN{ OFS=":" } /^:/ { match($1, /^:(.+) /, a); msg=a[1]; id=$2; printf "    .%s.: .%s.,\\n", msg, id }' | sort | tr . \\' | sed '$ s/,//'"""

#     process = subprocess.Popen(command, executable='bash',
#                                         shell=True,
#                                         stderr=subprocess.PIPE,
#                                         stdout=subprocess.PIPE)

#     data = process.stdout.read().decode()

#     if not data:
#         logging.fatal('Unable to acquire messages necessary to rebuild')
#         sys.exit(1)

#     exec('NEW_MSGLIST = {' + data + '}')

#     if eval('MSGLIST == NEW_MSGLIST'):
#         logging.info('Already up to date')
#         sys.exit(0)

#     logging.info('Rebuilding list now')

#     pattern = re.compile(r'^MSGLIST = {[^{^]*}', re.MULTILINE)

#     with open(__file__, 'rU') as self:
#         original = self.read()
#         replacement = pattern.sub('MSGLIST = {\n%s\n}' % data, original)

#     if replacement == original:
#         logging.fatal("Unable to rebuild '%s'... Is the file damaged?", __file__)
#         sys.exit(1)

#     # create a backup
#     subprocess.check_output("mv '{0}' '{0}.bak' &>/dev/null || sudo mv '{0}' '{0}.bak' &>/dev/null".format(__file__),
#                             executable='bash',
#                             shell=True)

#     # ensure backup was created
#     if not os.path.isfile(__file__ + '.bak'):
#         logging.fatal("Unable to create backup file '%s' prior to rebuild", __file__ + '.bak')
#         sys.exit(1)

#     try:
#         # create a temp file
#         tf = tempfile.NamedTemporaryFile()

#         # write data to temp file
#         tf.write(replacement.encode())

#         # ensure all data is written to temp file
#         tf.flush()

#         filewriter = """cat '{1}' | tee '{0}' &>/dev/null || cat '{1}' | sudo tee '{0}' &>/dev/null""".format(__file__, tf.name)

#         # write data to file
#         subprocess.check_output(filewriter,
#                                 executable='bash',
#                                 shell=True)
#     finally:
#         tf.close()

#     # check if file does not exist or is zero in size
#     if not os.path.isfile(__file__) or os.path.getsize(__file__) == 0:

#         logging.error("Failed to rebuild '%s'", __file__)

#         # delete empty file if it exists
#         if os.path.isfile(__file__):
#             subprocess.check_output("rm -f '{0}' &>/dev/null || sudo rm -f '{0}' &>/dev/null".format(__file__),
#                                     executable='bash',
#                                     shell=True)

#         # restore file from backup
#         subprocess.check_output("mv '{0}.bak' '{0}' &>/dev/null || sudo mv '{0}.bak' '{0}' &>/dev/null".format(__file__),
#                                 executable='bash',
#                                 shell=True)

#         sys.exit(1)

#     # set permissions using backup as a reference
#     subprocess.check_output("chmod --reference='{0}.bak' '{0}' &>/dev/null || sudo chmod --reference='{0}.bak' '{0}' &>/dev/null".format(__file__),
#                             executable='bash',
#                             shell=True)

#     # remove the backup
#     subprocess.check_output("rm -f '{0}.bak' &>/dev/null || sudo rm -f '{0}.bak' &>/dev/null".format(__file__),
#                             executable='bash',
#                             shell=True)

#     sys.exit(0)


def remove(path):
    """Remove file."""
    execute("rm -f '{0}' &>/dev/null || sudo rm -f '{0}' &>/dev/null".format(path))


def writer(source, destination):
    execute("""cat '{0}' | tee '{1}' &>/dev/null || cat '{0}' | sudo tee '{1}' &>/dev/null""".format(source, destination))


# configure logging
logging.basicConfig(format='%(levelname)s: %(message)s',
                    level=logging.INFO)

if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        add_help=False,
        prog=__program__,
        description=__description__,
        usage='%(prog)s [-b] MSGNAME')
    PARSER.add_argument(
        '-b', '--bare',
        action='store_true',
        dest='bare',
        help='display the message id ONLY')
    PARSER.add_argument(
        '-h', '--help',
        action='help',
        help=argparse.SUPPRESS)
    PARSER.add_argument(
        '--rebuild',
        action=RebuildAction,
        help='rebuild the message list',
        nargs=0)
    PARSER.add_argument(
        action='append',
        dest='msgnames',
        help=argparse.SUPPRESS,
        nargs='*')
    OPTIONS = PARSER.parse_args()
    MSGNAMES = OPTIONS.msgnames[0]

    if not MSGNAMES:
        print("%s: missing operand" % __program__, file=sys.stderr)
        print("Try '%s --help' for more information." % __program__, file=sys.stderr)
        sys.exit(1)

    PREFIX = '' if OPTIONS.bare else '# pylint: disable='

    RESULTS = [PREFIX + MSGLIST[m] for m in MSGNAMES if m in MSGLIST]

    if not RESULTS:
        sys.exit(1)

    print(*RESULTS, sep='\n')

    if len(RESULTS) < len(MSGNAMES):
        sys.exit(1)
