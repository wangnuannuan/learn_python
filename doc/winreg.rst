Windows registry access
#######################

**winreg.CloseKey(hkey)** 关闭打开的注册表

**winreg.OpenKey(key, sub_key, reserved=0, access=KEY_READ)**
**winreg.OpenKeyEx(key, sub_key, reserved=0, access=KEY_READ)**
打开指定key对应注册表，返回一个处理对象

**winreg.HKEY_CURRENT_USER**
**winreg.EnumValue(key, index)**

枚举打开的注册表项的值，返回元组,key是一个已经打开的键，或者是一个预定义的HKEY_ *常量。
index是一个整数，用于标识要检索的值的索引。
该函数每次调用时都会检索一个子项的名称。 通常会重复调用它，直到引发OSError异常，表示不再有值。

**winreg.QueryValueEx(key, value_name)** 检索与打开的注册表项关联的指定值名称的类型和数据
**winreg.SetValueEx(key, value_name, reserved, type, value)**