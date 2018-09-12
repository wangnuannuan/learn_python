from __future__ import print_function, absolute_import
import re
import os
from .. download_manager import (show_progress, hide_progress)
from tools.cmd import pquery, popen

regex_repo_url = r'^(git\://|file\://|ssh\://|https?\://|)(([^/:@]+)(\:([^/:@]+))?@)?([^/:]{3,})(\:\d+)?[:/](.+?)(\.git|\.hg|\/?)$'
regex_url_ref = r'^(.*/([\w.+-]+)(?:\.\w+)?)/?(?:#(.*))?$'
regex_local_ref = r'^([\w.+-][\w./+-]*?)/?(?:#(.*))?$'
very_verbose = False
git_cmd = 'git'
scms = {}

def formaturl(url, format="default"):
    url = "%s" % url
    m = re.match(regex_repo_url, url)
    if m and m.group(1) == '': # no protocol specified, probably ssh string like "git@github.com:xxx/osp.git"
        url = 'ssh://%s%s%s/%s' % (m.group(2) or 'git@', m.group(6), m.group(7) or '', m.group(8)) # convert to common ssh URL-like format
        m = re.match(regex_repo_url, url)

    if m:
        if format == "ssh":
            url = 'ssh://%s%s%s/%s' % (m.group(2) or 'git@', m.group(6), m.group(7) or '', m.group(8))
        elif format == "http":
            url = 'http://%s%s%s/%s' % (m.group(2) if (m.group(2) and (m.group(5) or m.group(3) != 'git')) else '', m.group(6), m.group(7) or '', m.group(8))
        elif format == "https":
            url = 'https://%s%s%s/%s' % (m.group(2) if (m.group(2) and (m.group(5) or m.group(3) != 'git')) else '', m.group(6), m.group(7) or '', m.group(8))
    return url


def scm(name):
    def _scm(cls):
        scms[name] = cls()
        return cls
    return _scm

def staticclass(cls):
    for k, v in cls.__dict__.items():
        if hasattr(v, '__call__') and not k.startswith('__'):
            setattr(cls, k, staticmethod(v))
    return cls

class ProcessException(Exception):
    pass

@scm('git')
@staticclass
class Git(object):
    name = 'git'
    default_branch = 'master'
    ignore_file = os.path.join('.git', 'info', 'exclude')

    def init(path=None):
        popen([git_cmd, 'init'] + ([path] if path else []) + ([] if very_verbose else ['-q']))

    def cleanup():
        print("Cleaning up Git index")
        pquery([git_cmd, 'checkout', '--detach', 'HEAD'] + ([] if very_verbose else ['-q'])) # detach head so local branches are deletable
        branches = []
        lines = pquery([git_cmd, 'branch']).strip().splitlines() # fetch all local branches
        for line in lines:
            if re.match(r'^\*?\s+\((.+)\)$', line):
                continue
            line = re.sub(r'\s+', '', line)
            branches.append(line)

        for branch in branches: # delete all local branches so the new repo clone is not poluted
            pquery([git_cmd, 'branch', '-D', branch])

    def clone(url, name=None, depth=None, protocol=None):
        if very_verbose:
            popen([git_cmd, 'clone', formaturl(url, protocol), name] + (['--depth', depth] if depth else []) + (['-v'] if very_verbose else ([] if verbose else ['-q'])))
        else:
            pquery([git_cmd, 'clone', '--progress', formaturl(url, protocol), name] + (['--depth', depth] if depth else []), output_callback=Git.action_progress)
            hide_progress()

    def add(dest):
        print("Adding reference "+dest)
        try:
            popen([git_cmd, 'add', dest] + (['-v'] if very_verbose else []))
        except ProcessException:
            pass

    def remove(dest):
        print("Removing reference "+dest)
        try:
            pquery([git_cmd, 'rm', '-f', dest] + ([] if very_verbose else ['-q']))
        except ProcessException:
            pass

    def commit(msg=None):
        popen([git_cmd, 'commit', '-a'] + (['-m', msg] if msg else []) + (['-v'] if very_verbose else ([] if verbose else ['-q'])))

    def publish(all_refs=None):
        if all_refs:
            popen([git_cmd, 'push', '--all'] + (['-v'] if very_verbose else ([] if verbose else ['-q'])))
        else:
            remote = Git.getremote()
            branch = Git.getbranch()
            if remote and branch:
                popen([git_cmd, 'push', remote, branch] + (['-v'] if very_verbose else ([] if verbose else ['-q'])))
            else:
                err = "Unable to publish outgoing changes for \"%s\" in \"%s\".\n" % (os.path.basename(getcwd()), getcwd())
                if not remote:
                    print(err+"The local repository is not associated with a remote one.", 1)
                if not branch:
                    print(err+"Working set is not on a branch.", 1)

    def fetch():
        print("Fetching revisions from remote repository to \"%s\"" % os.path.basename(getcwd()))
        popen([git_cmd, 'fetch', '--all', '--tags'] + (['-v'] if very_verbose else ([] if verbose else ['-q'])))

    def discard(clean_files=False):
        print("Discarding local changes in \"%s\"" % os.path.basename(getcwd()))
        pquery([git_cmd, 'reset', 'HEAD'] + ([] if very_verbose else ['-q'])) # unmarks files for commit
        pquery([git_cmd, 'checkout', '.'] + ([] if very_verbose else ['-q'])) # undo  modified files
        pquery([git_cmd, 'clean', '-fd'] + (['-x'] if clean_files else []) + (['-q'] if very_verbose else ['-q'])) # cleans up untracked files and folders

    def merge(dest):
        print("Merging \"%s\" with \"%s\"" % (os.path.basename(getcwd()), dest))
        popen([git_cmd, 'merge', dest] + (['-v'] if very_verbose else ([] if verbose else ['-q'])))

    def checkout(rev, clean=False):
        if not rev:
            return
        print("Checkout \"%s\" in %s" % (rev, os.path.basename(getcwd())))
        branch = None
        refs = Git.getbranches(rev)
        for ref in refs: # re-associate with a local or remote branch (rev is the same)
            m = re.match(r'^(.*?)\/(.*?)$', ref)
            if m and m.group(2) != "HEAD": # matches origin/<branch> and isn't HEAD ref
                if not os.path.exists(os.path.join('.git', 'refs', 'heads', m.group(2))): # okay only if local branch with that name doesn't exist (git will checkout the origin/<branch> in that case)
                    branch = m.group(2)
            elif ref != "HEAD":
                branch = ref # matches local branch and isn't HEAD ref

            if branch:
                print("Revision \"%s\" matches a branch \"%s\" reference. Re-associating with branch" % (rev, branch))
                popen([git_cmd, 'checkout', branch] + ([] if very_verbose else ['-q']))
                break

        if not branch:
            popen([git_cmd, 'checkout', rev] + (['-f'] if clean else []) + ([] if very_verbose else ['-q']))

    def update(rev=None, clean=False, clean_files=False, is_local=False):
        if not is_local:
            Git.fetch()
        if clean:
            Git.discard(clean_files)
        if rev:
            Git.checkout(rev, clean)
        else:
            remote = Git.getremote()
            branch = Git.getbranch()
            if remote and branch:
                try:
                    Git.merge('%s/%s' % (remote, branch))
                except ProcessException:
                    pass
            else:
                err = "Unable to update \"%s\" in \"%s\"." % (os.path.basename(getcwd()), getcwd())
                if not remote:
                    print(err+" The local repository is not associated with a remote one.")
                if not branch:
                    print(err+" Working set is not on a branch.")

    def status():
        return pquery([git_cmd, 'status', '-s'] + (['-v'] if very_verbose else []))

    def dirty():
        return pquery([git_cmd, 'status', '-uno', '--porcelain'])

    def untracked():
        return pquery([git_cmd, 'ls-files', '--others', '--exclude-standard']).splitlines()

    def outgoing():
        # Get default remote
        remote = Git.getremote()
        if not remote:
            return -1
        # Get current branch
        branch = Git.getbranch()
        if not branch:
            # Default to "master" in detached mode
            branch = "master"
        # Check if local branch exists. If not, then just carry on
        try:
            pquery([git_cmd, 'rev-parse', '%s' % branch])
        except ProcessException:
            return 0
        # Check if remote branch exists. If not, then it's a new branch
        try:
            if not pquery([git_cmd, 'rev-parse', '%s/%s' % (remote, branch)]):
                return 1
        except ProcessException:
            return 1
        # Check for outgoing commits for the same remote branch only if it exists locally and remotely
        return 1 if pquery([git_cmd, 'log', '%s/%s..%s' % (remote, branch, branch)]) else 0

    # Checks whether current working tree is detached
    def isdetached():
        return True if Git.getbranch() == "" else False

    # Finds default remote
    def getremote():
        remote = None
        remotes = Git.getremotes('push')
        for r in remotes:
            remote = r[0]
            # Prefer origin which is Git's default remote when cloning
            if r[0] == "origin":
                break
        return remote

    # Finds all associated remotes for the specified remote type
    def getremotes(rtype='fetch'):
        result = []
        remotes = pquery([git_cmd, 'remote', '-v']).strip().splitlines()
        for remote in remotes:
            remote = re.split(r'\s', remote)
            t = re.sub('[()]', '', remote[2])
            if not rtype or rtype == t:
                result.append([remote[0], remote[1], t])
        return result

    def seturl(url):
        print("Setting url to \"%s\" in %s" % (url, getcwd()))
        return pquery([git_cmd, 'remote', 'set-url', 'origin', url]).strip()

    def geturl():
        url = ""
        remotes = Git.getremotes()
        for remote in remotes:
            url = remote[1]
            if remote[0] == "origin": # Prefer origin URL
                break
        return formaturl(url)

    def getrev():
        return pquery([git_cmd, 'rev-parse', 'HEAD']).strip()

    # Gets current branch or returns empty string if detached
    def getbranch(rev='HEAD'):
        try:
            branch = pquery([git_cmd, 'rev-parse', '--symbolic-full-name', '--abbrev-ref', rev]).strip()
        except ProcessException:
            branch = "master"
        return branch if branch != "HEAD" else ""

    # Get all refs
    def getrefs():
        try:
            return pquery([git_cmd, 'show-ref', '--dereference']).strip().splitlines()
        except ProcessException:
            return []

    # Finds branches (local or remote). Will match rev if specified
    def getbranches(rev=None, ret_rev=False):
        result = []
        refs = Git.getrefs()
        for ref in refs:
            m = re.match(r'^(.+)\s+refs\/(heads|remotes)\/(.+)$', ref)
            if m and (not rev or m.group(1).startswith(rev)):
                result.append(m.group(1) if ret_rev else m.group(3))
        return result

    # Finds tags. Will match rev if specified
    def gettags():
        tags = []
        refs = Git.getrefs()
        for ref in refs:
            m = re.match(r'^(.+)\s+refs\/tags\/(.+)$', ref)
            if m:
                t = m.group(2)
                if re.match(r'^(.+)\^\{\}$', t): # detect tag "pointer"
                    t = re.sub(r'\^\{\}$', '', t) # remove "pointer" chars, e.g. some-tag^{}
                    for tag in tags:
                        if tag[1] == t:
                            tags.remove(tag)
                tags.append([m.group(1), t])
        return tags

    # Finds branches a rev belongs to
    def revbranches(rev):
        branches = []
        lines = pquery([git_cmd, 'branch', '-a', '--contains'] + ([rev] if rev else [])).strip().splitlines()
        for line in lines:
            if re.match(r'^\*?\s+\((.+)\)$', line):
                continue
            line = re.sub(r'\s+', '', line)
            branches.append(line)
        return branches

    def ignores():
        try:
            ignore_file_parent_directory = os.path.dirname(Git.ignore_file)
            if not os.path.exists(ignore_file_parent_directory):
                os.mkdir(ignore_file_parent_directory)

            with open(Git.ignore_file, 'w') as f:
                f.write('\n'.join(ignores)+'\n')
        except IOError:
            print("Unable to write ignore file in \"%s\"" % os.path.join(getcwd(), Git.ignore_file), 1)

    def ignore(dest):
        try:
            with open(Git.ignore_file) as f:
                exists = dest in f.read().splitlines()
        except IOError:
            exists = False

        if not exists:
            try:
                ignore_file_parent_directory = os.path.dirname(Git.ignore_file)
                if not os.path.exists(ignore_file_parent_directory):
                    os.mkdir(ignore_file_parent_directory)

                with open(Git.ignore_file, 'a') as f:
                    f.write(dest.replace("\\", "/") + '\n')
            except IOError:
                print("Unable to write ignore file in \"%s\"" % os.path.join(getcwd(), Git.ignore_file), 1)
    def unignore(dest):
        try:
            with open(Git.ignore_file) as f:
                lines = f.read().splitlines()
        except IOError:
            lines = []

        if dest in lines:
            lines.remove(dest)
            try:
                ignore_file_parent_directory = os.path.dirname(Git.ignore_file)
                if not os.path.exists(ignore_file_parent_directory):
                    os.mkdir(ignore_file_parent_directory)

                with open(Git.ignore_file, 'w') as f:
                    f.write('\n'.join(lines) + '\n')
            except IOError:
                print("Unable to write ignore file in \"%s\"" % os.path.join(getcwd(), Git.ignore_file), 1)

    def action_progress(line, sep):
        m = re.match(r'([\w :]+)\:\s*(\d+)% \((\d+)/(\d+)\)', line)
        if m:
            if m.group(1) == "remote: Compressing objects" and int(m.group(4)) > 100:
                show_progress('Preparing', (float(m.group(3)) / float(m.group(4))) * 100)
            if m.group(1) == "Receiving objects":
                show_progress('Downloading', (float(m.group(3)) / float(m.group(4))) * 80)
            if m.group(1) == "Resolving deltas":
                show_progress('Downloading', (float(m.group(3)) / float(m.group(4))) * 10 + 80)
            if m.group(1) == "Checking out files":
                show_progress('Downloading', (float(m.group(3)) / float(m.group(4))) * 10 + 90)

ignores = [
    # Version control folders
    ".hg",
    ".git",
    ".svn",
    ".CVS",
    ".cvs",

    # Version control fallout
    "*.orig",

    # mbed Tools
    "BUILD",
    ".build",
    ".export",

    # Online IDE caches
    ".msub",
    ".meta",
    ".ctags*",

    # uVision project files
    "*.uvproj",
    "*.uvopt",

    # Eclipse project files
    "*.project",
    "*.cproject",
    "*.launch",

    # IAR project files
    "*.ewp",
    "*.eww",

    # GCC make
    "/Makefile",
    "Debug",

    # HTML files
    "*.htm",

    # Settings files
    "*.settings",

    # Python
    "*.py[cod]",
    "# subrepo ignores",
    ]
