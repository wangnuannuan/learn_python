
fs plus npm

```getHomeDirectory()``` 返回相对于home的绝对路径
```absolute(relativePath)``` 返回绝对路径，如果路径以```~``开头，会被转化成相对于用户home的路径
```normalize(pathToNormalize)```路径转换成符合当前系统格式的路径
```tildify(pathToTildify)```  将路径转化成以`~`开头的路径
`getSizeSync(pathToCheck)` 返回文件大小
古人云：“君子一诺千金”，这种“承诺将来会执行”的对象在JavaScript中称为Promise对象。
Promise有各种开源实现，在ES6中被统一规范，由浏览器直接支持。
``

'use strict';

// 清除log:
var logging = document.getElementById('test-promise-log');
while (logging.children.length > 1) {
    logging.removeChild(logging.children[logging.children.length - 1]);
}

// 输出log到页面:
function log(s) {
    var p = document.createElement('p');
    p.innerHTML = s;
    logging.appendChild(p);
}

new Promise(function (resolve, reject) {
    log('start new Promise...');
    var timeOut = Math.random() * 2;
    log('set timeout to: ' + timeOut + ' seconds.');
    setTimeout(function () {
        if (timeOut < 1) {
            log('call resolve()...');
            resolve('200 OK');
        }
        else {
            log('call reject()...');
            reject('timeout in ' + timeOut + ' seconds.');
        }
    }, timeOut * 1000);
}).then(function (r) {
    log('Done: ' + r);
}).catch(function (reason) {
    log('Failed: ' + reason);
});

```

`...` Spread 扩展运算符


将一个数组转为用逗号分隔的参数序列

```
//扩展运算符取代apply方法的一个实际的例子，应用Math.max方法，简化求出一个数组最大元素的写法。
// ES5 的写法
Math.max.apply(null, [14, 3, 77])
 
// ES6 的写法
Math.max(...[14, 3, 77])
 
// 等同于
Math.max(14, 3, 77);
```

tmp npm

创建临时文件和目录


spawn 和 exec 的区别
总体来说 spawn 返回一个stream，exec返回一个buffer
child_process.spawn 返回一个有输出流和错误的流的对象，你可以监听它们从而获取数据，输出流有数据和结束事件，child_process.spawn 适合用在处理大量数据返回的场景中，图片处理，读二进制数据等等。
child_process.spawn是一个异步的异步函数，怎么解释呢？child_process.spawn 在执行时就会返回数据，而不是等到数据都处理好了再一次返回。
child_process.exec 一次性返回输出执行结果内容，默认的buffer大小为200kb，如果exec返回的内容超过 200kb则会返回一个错误：Error maxBuffer execeded，你可以通过设置options buffer的size来扩大 buffer 的大小。
child_process.exec 是一个同步的异步方法，这个意思是，虽然方法体本身是异步的，但是它要等 child process 执行完成后，再把返回数据一口气返回给回调方法。如果返回内容超过了设置的buffer size，则会返回一个maxBuffer exceeded 错误

Node.js 的子进程 (child_process) 模块下有一 spawn 函数，可以用于调用系统上的命令，如在 Linux, macOS 等系统上，我们可以执行
```
const spawn = require('child_process').spawn;
 
spawn('npm', {
 stdio: 'inherit'
});
```

SocketJS
一、定义

SockJS是一个浏览器JavaScript库，它提供了一个类似于网络的对象。SockJS提供了一个连贯的、跨浏览器的Javascript API，它在浏览器和web服务器之间创建了一个低延迟、全双工、跨域通信通道。



二、产生的原因

一些浏览器中缺少对WebSocket的支持,因此，回退选项是必要的，而Spring框架提供了基于SockJS协议的透明的回退选项。

SockJS的一大好处在于提供了浏览器兼容性。优先使用原生WebSocket，如果在不支持websocket的浏览器中，会自动降为轮询的方式。 
除此之外，spring也对socketJS提供了支持。

如果代码中添加了withSockJS()如下，服务器也会自动降级为轮询。



registry.addEndpoint("/coordination").withSockJS();1

SockJS的目标是让应用程序使用WebSocket API，但在运行时需要在必要时返回到非WebSocket替代，即无需更改应用程序代码。

SockJS是为在浏览器中使用而设计的。它使用各种各样的技术支持广泛的浏览器版本。对于SockJS传输类型和浏览器的完整列表，可以看到SockJS客户端页面。 
传输分为3类:WebSocket、HTTP流和HTTP长轮询（按优秀选择的顺序分为3类）

jsonrpc-lite npm

在浏览器中解析JSON_RPC2信息

tcp-port-used npm

检测当前正在使用的TCP端口


JavaScript Snippets for Atom

zlib npm

语义化版本控制规范（SemVer）