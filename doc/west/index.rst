

cmd
####

- init.py
	- class WestCommand(ABC)：# 定义抽象类
		- self.name 命令名
		- self.description 命令描述
		- self._accept_unknown 如果是True,可以通过方法run()运行位置参数的命令
	- def run(self, args, unknown):调用do_run运行命令
	- def add_parser(self, parser_adder)调用do_add_parse添加命令行参数
	
