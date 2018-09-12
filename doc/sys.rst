sys

**sys._getframe(0)** 获取当前栈信息
sys._getframe(0).f_code.co_filename   # 当前文件名，也可以通过__file__获得
sys._getframe(0).f_code.co_name   # 当前函数名
sys._getframe(0).f_lineno   # 当前行号
sys._getframe(1).f_locals  #来获得局部变量

collection

namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。

使用list存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为list是线性存储，数据量大的时候，插入和删除效率很低
deque除了实现list的append()和pop()外，还支持appendleft()和popleft()，这样就可以非常高效地往头部添加或删除元素
使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict

``
from collections import defaultdict
dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
dd['key1'] # key1存在
'abc'
dd['key2'] # key2不存在，返回默认值
'N/A'``

OrderedDict的Key会按照插入的顺序排列，不是Key本身排序
OrderedDict可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key
Counter是一个简单的计数器,Counter实际上也是dict的一个子类

os

os.path.sep路径分隔符

Python 有一个 bisect 模块，用于维护有序列表。bisect 模块实现了一个算法用于插入元素到有序列表。在一些情况下，这比反复排序列表或构造一个大的列表再排序的效率更高。Bisect 是二分法的意思，这里使用二分法来排序，它会将一个元素插入到一个有序列表的合适位置，这使得不需要每次调用 sort 的方式维护有序列表

yaml

load() 读取yaml文件
load_all() 读取多个文件，生成迭代器

dump将pyrhon对象转换成yaml文档

del删除变量，解除对数据的引用
