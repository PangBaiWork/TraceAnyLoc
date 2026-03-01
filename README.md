## TraceAnyLoc (TAL)
跨平台的高性能任意地址的Trace工具 

多平台统一日志格式，可自定义绕过多种导致控制流中断的代码(异常/中断等)，可用于控制流分析/VMP分析/混淆分析等常见二进制分析场景。
- 指令执行前后寄存器监控
- 内存读写监控
- 可打印字符串读写监控
- 支持任意地址进入
- 任意地址退出
- 支持任意地址范围逃离/返回。
- 自动上下文同步 


[![QQ](https://img.shields.io/badge/Join-QQ_Group-ff69b4)](https://qm.qq.com/q/1wJcBUfst2)

支持平台：Windows、Linux、Android (均仅支持64位)
注：因为没有相关硬件设备，暂未支持Ios和MacOS。
日志格式如下：
```
0x1487e0:	str	x9, [sp]                   SP=0x6e74884ff0  X9=0x5  | 
MemoryWrite:[0x6e74884ff0] <0x8> 
0x1487e4:	br	x8                          X8=0x6e0f0477e8  | 
0x1487e8:	ldr	x8, [sp]                   SP=0x6e74884ff0  X8=0x6e0f0477e8  |  X8=0x5 
MemoryRead:[0x6e74884ff0] <0x8> 
0x1487ec:	str	x8, [sp, #0x28]            SP=0x6e74884ff0  X8=0x5  | 
MemoryWrite:[0x6e74885018] <0x8> 
0x1487f0:	ldr	x8, [sp, #0x28]            SP=0x6e74884ff0  X8=0x5  |  X8=0x5 
MemoryRead:[0x6e74885018] <0x8> 
0x1487f4:	add	x8, x19, x8                X8=0x5  X19=0x71e27be720  X8=0x5  |  X8=0x71e27be725 
0x1487f8:	ldrb	w8, [x8]                  X8=0x71e27be725  X8=0x71e27be725  |  X8=0x4d 
PrintableRead:[M007xAAgI906hmu6n/68CNfYI9wiThHdhjuQFnQSU9u+zQ8uyH/T1lKs/8MaY/NsZHpJ62Uyps0LCK7BN7E2eCPcVrQv2CPcI]
0x1487fc:	strb	w8, [sp, #0x24]           SP=0x6e74884ff0  X8=0x4d  | 
MemoryWrite:[0x6e74885014] <0x1> 
```
## 静态ELF文件的分析
静态ELF文件在二进制注入时存在特殊之处，无法直接使用本工具套件。 

可使用 [StaticElfLoader](https://github.com/PangBaiWork/StaticElfLoader) 加载运行后再使用本工具分析。
## 开始使用
安装依赖(尽可能使用以下版本的Frida)
```bash
pip install frida==16.7.15  
pip install frida-tools==13.7.1
```
本仓库`test`文件夹存放三种使用脚本，需要按需修改。 

`cli_trace_linux.py`使用`trace_input.js`，日志会存在于子文件夹`linux`下。 

`cli_trace_windows.py`使用`trace_input2.js`，日志会存在于子文件夹`windows`下。 

安卓平台需使用`trace_input3.js`，由于案例过于敏感，本处不做过多解释。 

各个脚本中都存在 `start_trace` 函数，此函数需要`hook`一个地址来初始化 `Trace`的设置 (此地址一定要在`Trace`启动之前被执行到)。`trace`函数有四个参数，第一个模块对象，第二个设置`Trace`启动地址，第三个参数设置`trace`结束地址，第四个参数为常数。

测试使用 `浙江省网安省赛赛题 - Warning` 以及 `N1CTF Junior 2025 - TrueOperator` 进行测试，侵联则删。 
## 开源许可证
本仓库的二进制静态链接自多个第三方库，并在遵循各个开源协议的前提下进行分发。 

详细可见本项目附件 [COPYING](COPYING)