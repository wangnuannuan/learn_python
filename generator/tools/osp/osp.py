from __future__ import print_function, division, absolute_import
from tools.download_manager import generate_yaml, edit_yaml, getcwd
from tools.notify import TerminalNotifier
from tools.settings import *
import yaml
import os
class OSP(object):
    def __init__(self, file="osp.yaml"):
        self.path = os.path.join(os.path.expanduser("~"), '.embarc_cli')
        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path)
            except (IOError, OSError):
                pass
        self.file = file

        fl = os.path.join(self.path, self.file)
        if not os.path.exists(fl):
            self.cfg_dict = dict()
            self.cfg_dict["path"] = dict()
            generate_yaml(fl, self.cfg_dict)
        else:
            self.cfg_dict = yaml.load(fl)

    def set_path(self, url, path):
        fl = os.path.join(self.path, self.file)
        try:
            with open(fl) as f:
                self.cfg_dict = yaml.load(f)
                for key, path_dict  in self.cfg_dict.items():
                    for url_, path_ in path_dict:
                        if url==url_ and path==path_ :
                            return
                path_num = len(self.cfg_dict)
                path_key = "path" + str(path_num + 1)
                self.cfg_dict[path_key] = dict()
                self.cfg_dict[path_key]["url"] = url
                self.cfg_dict[path_key]["path"] = path
                edit_yaml(fl, self.cfg_dict)

        except IOError:
            raise IOError("Can not open file %s ." % fl)

    def get_path(self):
        fl = os.path.join(self.path, self.file)
        try:
            with open(fl) as f:
                self.cfg_dict = yaml.load(f)
                for path, path_dict  in self.cfg_dict.items():
                    if path_dict.get("path", None):
                        osp_root = path_dict["path"]
                        if self.is_osp(osp_root):
                            return osp_root
                return None

        except IOError:
            raise IOError("Can not open file %s ." % fl)
    def clear_path(self):
        fl = os.path.join(self.path, self.file)
        try:
            with open(fl) as f:
                self.cfg_dict = dict()
                edit_yaml(fl, self.cfg_dict)

        except IOError:
            raise IOError("Can not open file %s ." % fl)

    def list_path(self):
        fl = os.path.join(self.path, self.file)
        try:
            with open(fl) as f:
                self.cfg_dict = yaml.load(f)

                table_head = ["osp"]
                table_content = list()
                for path, path_dict in self.cfg_dict.items():
                    table_content.append([path])
                    string_list = [ " %s: %s" % (key, value) for (key, value) in path_dict.items()]
                    string = "\n".join(string_list)
                    table_content.append([string])
                notifier = TerminalNotifier()
                notifier.event["format"] = "table"
                notifier.event["message"] = [table_head, table_content]

                notifier.notify(notifier.event)

        except IOError:
            raise IOError("Can not open file %s ." % fl)

    def is_osp(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            for files in OSP_DIRS:
                files_path = os.path.join(path, files)
                if os.path.exists(files_path) and os.path.isdir(files_path):
                    pass
                else:
                    return False
            return True
        else:
            return False

    def support_board(self, root):
        result = []
        board_path = os.path.join(root, "board")
        if os.path.exists(board_path):
            for file in os.listdir(board_path):
                if os.path.isdir(os.path.join(board_path, file)):
                    result.append(file)
        return result

    def get_board_version(self, root, board, bd_version=None):
        result = []
        board_path = "board/" + board
        ver_path = os.path.join(root, board_path)
        if os.path.exists(ver_path):
            bd_vers_dict = self._board_version_config(root, board, bd_version)
            result.extend(bd_vers_dict.keys())
        return result

    def _board_version_config(self, root, board, bd_version=None):
        board_path = os.path.join(root, "board", board)
        bd_vers = dict()
        if os.path.exists(board_path):
            files = os.listdir(board_path)
            if "configs" in files:
                versions = os.listdir(os.path.join(board_path, "configs"))
                for version in versions:
                    version_path = os.path.join(board_path, "configs", version)
                    if os.path.isdir(version_path):
                        bd_vers[version] = version_path
            else:
                versions = os.listdir(board_path)
                for version in versions:
                    path = os.path.join(board_path, version)
                    if os.path.isdir(path) and "configs" in os.listdir(path):
                        version_path = os.path.join(board_path, version, "configs")
                        bd_vers[version] = version_path
        if bd_version is not None:
            if bd_version in bd_vers:
                bd_ver = {bd_version: bd_vers[bd_version]}
                return bd_ver
        return bd_vers

    def get_tcfs(self, root, board, bd_version, cur_core=None):
        result = []
        board_version_path_dict = self._board_version_config(root, board, bd_version)
        board_path = board_version_path_dict[bd_version]

        if os.path.exists(board_path):
            if cur_core:
                cur_core_file = cur_core + ".tcf"
                for root, dirs, files in os.walk(board_path, topdown=True):
                    if cur_core_file in files:
                        result.append(cur_core)

            else:

                for root, dirs, files in os.walk(board_path, topdown=True):

                    for file in files:
                        filename, filesuffix = os.path.splitext(file)
                        if not filesuffix == ".tcf":
                            continue
                        result.append(filename)

        return result

    def get_makefile(self, app_path):
        for makefile in MakefileNames:
            makefile_path = os.path.join(app_path, makefile)
            if os.path.exists(makefile_path) and os.path.isfile(makefile_path):
                return makefile_path
        return None
