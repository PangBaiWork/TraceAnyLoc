## TraceAnyLoc (TAL)
跨平台的高性能任意地址的Trace工具 

多平台统一日志格式，可自定义绕过多种导致控制流中断的代码(异常/中断等)，可用于控制流分析/VMP分析/混淆分析等常见二进制分析场景。
- 全平台函数调用符号
- 函数调用参数打印 (指针自动hexdump)
- 自实现污点分析
- Triton污点分析
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
Trace模式:
```
ADDR: 污点跟踪模式, 
BIN: 带指令HEX的Trace模式, 
DEBUG: 带额外调试信息的模式,
TRACE: 通用Trace模式, 
TRITON: Triton污点跟踪模式(极慢), 
TRACE_ARGS: 带函数调用参数打印的Trace模式,
```
Trace格式:
```
模块:偏移:指令  执行前寄存器|执行后寄存器|内存读写[读写地址]="字符串"/HEX
```
功能函数
```
set_function_print(count,len) // 设置TRACE_ARGS模式默认打印参数个数和Hexdump长度,CPP函数会自动解析参数不受个数限制
set_taint_str(str) // 设置污点化的字符串内容，在CTF中为测试的字符串即可
trace(start,end,1,mode) // 设置trace启动和结束地址和trace模式
set_log_path(path) //日志输出地址，不设置默认当前目录，安卓需要特别设置
```
日志示例
```asm
Warning:0x112c:	mov	ecx, 0x80                      RCX=0x55c7dd4e3210 | RCX=0x80 |
Warning:0x1131:	mov	rdx, rbx                       RBX=0x10a RDX=0x1 | RDX=0x10a |
Warning:0x1134:	mov	esi, 0x1                       RSI=0x10a | RSI=0x1 |
Warning:0x1139:	rep		stosq	qword ptr es:[rdi], rax RAX=0x0 RDI=0x7ffca9274520 RDI=0x7ffca9274520 | RDI=0x7ffca9274920 | W[0x7ffca9274520]=0x0 <0x400> 
Warning:0x113c:	mov	rcx, rbp                       RBP=0x55c7dd4e3130 RCX=0x0 | RCX=0x55c7dd4e3130 |
Warning:0x113f:	mov	rdi, r14                       R14=0x7ffca9274520 RDI=0x7ffca9274920 | RDI=0x7ffca9274520 |
Warning:0x1142:	call	-0x107                        RSP=0x7ffca9274520 | RSP=0x7ffca9274518 |
call Warning:0x1040
Warning:0x1040:	jmp	qword ptr [rip + 0x2f62]       RIP=0x55c7c4f78040 | |
call libc.so.6:fread R[0x55c7c4f7afa8]=0x7fd28266f300 <0x8> 
Warning:0x1147:	mov	rdx, rbx                       RBX=0x10a RDX=0x1 | RDX=0x10a |
Warning:0x114a:	mov	rsi, r14                       R14=0x7ffca9274520 RSI=0x55c7dd4e33b0 | RSI=0x7ffca9274520 |
Warning:0x114d:	mov	rdi, r12                       R12=0x7ffca9274920 RDI=0x55c7dd4e3210 | RDI=0x7ffca9274920 |
```
Trace_args模式:
```asm
libark_jsruntime.so:0x20145e7:	mov	r13, qword ptr [rbp + 8*rbx] RBX=0x5ce RBP=0x55ad1ccc3740 R13=0x55ad1ccdb2b0 | R13=0x0 | R[0x55ad1ccc65b0]=0x0 <0x8> 
libark_jsruntime.so:0x20145ec:	test	r13, r13                   R13=0x0 R13=0x0 | |
libark_jsruntime.so:0x20145ef:	mov	qword ptr [rsp + 0x40], rbp RBP=0x55ad1ccc3740 RSP=0x7ffdc4e30e20 | | W[0x7ffdc4e30e60]=0x55ad1ccc3740 <0x8> 
libark_jsruntime.so:0x20145f4:	jne	0x40                        | |
libark_jsruntime.so:0x20145f6:	mov	edi, 0x40                   RDI=0x55ad1cd65690 | RDI=0x40 |
libark_jsruntime.so:0x20145fb:	call	0x6ce370                   RSP=0x7ffdc4e30e20 | RSP=0x7ffdc4e30e18 |
call libark_jsruntime.so:0x26e2970
demangled : 0x26e2970
argc      : 3 default(3) reason=c_or_unmangled_symbol
arg[0] = 0x40
arg[1] = 0x26
arg[2] = 0x7b4c2a71

libark_jsruntime.so:0x26e2970:	jmp	qword ptr [rip + 0x581f2]   RIP=0x7fef494e2970 | |
call libstdc++.so.6.0.34:_Znwm
demangled : operator new(unsigned long)
argc      : 2 reason=demangled
arg[0] = 0x40
arg[1] = 0x26
```
windows
```asm
TrueOperator.exe:0x700d0:	mov	qword ptr [rsp + 0x68], rdx   RDX=0x9a19fff810 RSP=0x9a19fff700 | | W[0x9a19fff768]=0x9a19fff810 <0x8> 
TrueOperator.exe:0x700d5:	mov	qword ptr [rsp + 0x70], r8    R8=0x7ffa4dfa0990 RSP=0x9a19fff700 | | W[0x9a19fff770]=0x7ffa4dfa0990 <0x8> 
TrueOperator.exe:0x700da:	mov	qword ptr [rsp + 0x78], r9    R9=0x0 RSP=0x9a19fff700 | | W[0x9a19fff778]=0x0 <0x8> 
TrueOperator.exe:0x700df:	mov	qword ptr [rsp + 0x38], rsi   RSI=0x9a19fff768 RSP=0x9a19fff700 | | W[0x9a19fff738]=0x9a19fff768 <0x8> 
TrueOperator.exe:0x700e4:	call	0x2c7                        RSP=0x9a19fff700 | RSP=0x9a19fff6f8 |
call TrueOperator.exe:0x703b0
TrueOperator.exe:0x703b0:	jmp	qword ptr [rip + 0xf03a]      RIP=0x7ff783e003b0 | |
call ucrtbase.dll:__acrt_iob_func R[0x7ff783e0f3f0]=0x7ffa4dec7d40 <0x8> 
TrueOperator.exe:0x700e9:	mov	qword ptr [rsp + 0x20], rsi   RSI=0x9a19fff768 RSP=0x9a19fff700 | | W[0x9a19fff720]=0x9a19fff768 <0x8> 
TrueOperator.exe:0x700ee:	xor	r9d, r9d                      R9=0x0 R9=0x0 | R9=0x0 |
TrueOperator.exe:0x700f1:	mov	r8, rbx                       RBX=0x7ff783e02012 R8=0x7ffa4dfa0990 | R8=0x7ff783e02012 |
TrueOperator.exe:0x700f4:	mov	rdx, rax                      RAX=0x7ffa4df9f4a0 RDX=0x9a19fff810 | RDX=0x7ffa4df9f4a0 |
TrueOperator.exe:0x700f7:	xor	ecx, ecx                      RCX=0x7ffa4df9f4a0 RCX=0x7ffa4df9f4a0 | RCX=0x0 |
TrueOperator.exe:0x700f9:	call	0x2d2                        RSP=0x9a19fff700 | RSP=0x9a19fff6f8 |
call TrueOperator.exe:0x703d0
TrueOperator.exe:0x703d0:	jmp	qword ptr [rip + 0xf03a]      RIP=0x7ff783e003d0 | |
call ucrtbase.dll:__stdio_common_vfscanf R[0x7ff783e0f410]=0x7ffa4df28900 <0x8> 
TrueOperator.exe:0x700fe:	add	rsp, 0x48                     RSP=0x9a19fff700 | RSP=0x9a19fff748 |
TrueOperator.exe:0x70102:	pop	rbx                           RBX=0x7ff783e02012 RSP=0x9a19fff748 | RBX=0x10 RSP=0x9a19fff750 | R[0x9a19fff748]=0x10 <0x8> 
TrueOperator.exe:0x70103:	pop	rsi                           RSI=0x9a19fff768 RSP=0x9a19fff750 | RSI=0x32 RSP=0x9a19fff758 | R[0x9a19fff750]=0x32 <0x8> 
TrueOperator.exe:0x70104:	ret                               RSP=0x9a19fff758 | RSP=0x9a19fff760 | R[0x9a19fff758]=0x7ff783dfee31 <0x8> 
TrueOperator.exe:0x6ee31:	lea	rax, [rbp - 0x40]             RBP=0x9a19fff850 RAX=0x1 | RAX=0x9a19fff810 |
TrueOperator.exe:0x6ee35:	mov	rcx, rax                      RAX=0x9a19fff810 RCX=0xffffffff | RCX=0x9a19fff810 |
TrueOperator.exe:0x6ee38:	call	0x1563                       RSP=0x9a19fff760 | RSP=0x9a19fff758 |
call TrueOperator.exe:0x703a0
TrueOperator.exe:0x703a0:	jmp	qword ptr [rip + 0xf092]      RIP=0x7ff783e003a0 | |
call ucrtbase.dll:strlen R[0x7ff783e0f438]=0x7ffa4decc9f0 <0x8> 
```
android
```asm
libhookme.so:0xcbd30:   ldur    x0, [x29, #-0x8]             X29=0x7ffbed5e80 X0=0xb400007d8e496d00 | X0=0xb400007d8e496d00 | R[0x7ffbed5e78]=0xb400007d8e496d00 <0x8>
libhookme.so:0xcbd34:   ldr     x8, [x0]                      X0=0xb400007d8e496d00 X8=0x0 | X8=0x7d852207f8 | R[0xb400007d8e496d00]=0x7d852207f8 <0x8>
libhookme.so:0xcbd38:   ldr     x8, [x8, #0x388]              X8=0x7d852207f8 X8=0x7d852207f8 | X8=0x7d84e96754 | R[0x7d85220b80]=0x7d84e96754 <0x8>
libhookme.so:0xcbd3c:   ldr     x1, [sp, #0x10]               SP=0x7ffbed5e60 X1=0x7c8007eb00 | X1=0x7c8007eb00 | R[0x7ffbed5e70]=0x7c8007eb00 <0x8>
libhookme.so:0xcbd40:   ldr     x2, [sp, #0x8]                SP=0x7ffbed5e60 X2=0x7c28b0cfa4 | X2=0x7c28b0cfa4 | R[0x7ffbed5e68]=0x7c28b0cfa4 <0x8>
libhookme.so:0xcbd44:   ldr     x3, [sp]                      SP=0x7ffbed5e60 X3=0x7c28b0ba3f | X3=0x7c28b0ba3f | R[0x7ffbed5e60]=0x7c28b0ba3f <0x8>
libhookme.so:0xcbd48:   blr     x8                            SP=0x7ffbed5e60 X8=0x7d84e96754 LR=0x7c28b85aec | LR=0x7c28b85d4c |
call libart.so:_ZN3art12_GLOBAL__N_18CheckJNI17GetStaticMethodIDEP7_JNIEnvP7_jclassPKcS7_.__uniq.99033978352804627313491551960229047428.llvm.14675227012795551090
demangled : art::(anonymous namespace)::CheckJNI::GetStaticMethodID(_JNIEnv*, _jclass*, char const*, char const*) (.__uniq.99033978352804627313491551960229047428.llvm.14675227012795551090)
argc      : 5 reason=demangled
arg[0] = 0xb400007d8e496d00 -> 0x7d8e496d00:
7d8e496d00000000  f8 70 22 85 7d 00 00 00  00 8c 55 8e 7d 00 00 b4  |..".}.....U.}...|
7d8e496d10000000  c0 d6 46 8e 7d 00 00 b4  80 00 00 00 80 00 00 00  |..F.}...........|
7d8e496d20000000  00 20 00 00 1d 00 00 00  00 00 00 00 00 00 00 00  |................|
7d8e496d30000000  c0 d0 4b 8e 7d 00 00 b4  d8 d0 4b 8e 7d 00 00 b4  |..K.}.....K.}...|
arg[1] = 0x7c8007eb00:
7c8007eb00000000  30 77 40 20 90 10 20 10  33 00 00 00 30 00 fe ff  |0w@... .3.......|
7c8007eb10000000  60 5a b8 28 7c 00 00 00  30 75 8d 84 7d 00 00 00  |`Z.(|...0u..}...|
7c8007eb20000000  30 77 40 20 90 00 38 10  35 00 00 00 40 00 ff ff  |0w@...8.5.......|
7c8007eb30000000  cc 54 6b 3b 7e 00 00 00  e0 77 8d 84 7d 00 00 00  |.Tk;~....w..}...|
arg[2] = 0x7c28b0cfa4:
7c28b0cfa4000000  6a 61 76 61 43 61 6c 6c  62 61 63 6b 00 31 31 34  |javaCallback.114|
7c28b0cfb4000000  35 31 34 34 34 34 34 34  34 31 31 31 31 00 61 6c  |5144444441111.al|
7c28b0cfc4000000  6e 75 6d 00 49 53 32 00  64 6f 6c 6c 61 72 2d 73  |num.IS2.dollar-s|
7c28b0cfd4000000  69 67 6e 00 72 69 67 68  74 2d 63 75 72 6c 79 2d  |ign.right-curly-|
arg[3] = 0x7c28b0ba3f:
7c28b0ba3f000000  28 4c 6a 61 76 61 2f 6c  61 6e 67 2f 53 74 72 69  |(Ljava/lang/Stri|
7c28b0ba4f000000  6e 67 3b 29 56 00 76 65  72 74 69 63 61 6c 2d 74  |ng;)V.vertical-t|
7c28b0ba5f000000  61 62 00 53 49 00 46 72  69 64 61 79 00 73 74 64  |ab.SI.Friday.std|
7c28b0ba6f000000  3a 3a 62 61 64 5f 61 6c  6c 6f 63 00 6f 75 74 2f  |::bad_alloc.out/|
arg[4] = 0x7c28b07b34:
7c28b07b34000000  00 62 61 73 69 63 5f 73  74 72 69 6e 67 00 61 6c  |.basic_string.al|
7c28b07b44000000  70 68 61 00 46 46 00 44  4c 45 00 63 6f 6d 6d 61  |pha.FF.DLE.comma|
7c28b07b54000000  00 70 65 72 69 6f 64 00  77 65 00 4d 6f 6e 00 46  |.period.we.Mon.F|
7c28b07b64000000  65 62 00 4a 75 6e 00 74  65 72 6d 69 6e 61 74 69  |eb.Jun.terminati|

libhookme.so:0x206940:  adrp    x16, #53248                 X16=0x1 | X16=0x7c28ccd000 |
libhookme.so:0x206944:  ldr     x17, [x16, #0xa30]           X16=0x7c28ccd000 X17=0x7e3a8f4080 | X17=0x7e3a90bc38 | R[0x7c28ccda30]=0x7e3a90bc38 <0x8>
libhookme.so:0x206948:  add     x16, x16, #0xa30             X16=0x7c28ccd000 X16=0x7c28ccd000 | X16=0x7c28ccda30 |
libhookme.so:0x20694c:  br      x17                           X17=0x7e3a90bc38 | |
call libc.so:__strlen_chk
demangled : __strlen_chk
argc      : 3 default(3) reason=c_or_unmangled_symbol
arg[0] = 0xb400007ccbbffc28 -> 0x7ccbbffc28:
7ccbbffc28000000  31 31 31 34 00 00 00 b4  10 f5 b2 10 64 93 30 00  |1114........d...|
7ccbbffc38000000  af 8e d3 20 a8 8e d3 20  28 8c 25 30 64 93 30 00  |........(.%.d...|
7ccbbffc48000000  00 c2 bf c6 7c 00 00 b4  10 00 00 00 00 00 00 b4  |....|...........|
7ccbbffc58000000  00 72 be c6 7c 00 00 b4  00 72 be c6 7c 00 00 b4  |.r..|....r..|...|
arg[1] = 0xffffffffffffffff
arg[2] = 0xb400007d8e558c00 -> 0x7d8e558c00:
7d8e558c00000000  00 00 00 5c 00 00 00 00  10 00 00 00 50 3b 00 00  |...\.........;..|
7d8e558c10000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
7d8e558c20000000  00 00 00 00 00 00 00 00  00 00 00 00 10 00 00 00  |................|
7d8e558c30000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|

```
## 开始使用
安装依赖
```bash
pip install frida
pip install frida-tools
```
本仓库`test`文件夹存放三种使用脚本，需要按需修改。 
### Linux
`cli_trace_linux.py`使用`trace_input_linux.js`，修改后直接执行即可。  
静态ELF文件在二进制注入时存在特殊之处，无法直接使用本工具套件。  
可使用 [StaticElfLoader](https://github.com/PangBaiWork/StaticElfLoader) 加载运行后再使用本工具分析。 
### Windows
`cli_trace_windows.py`使用`trace_input_windows.js`，修改后直接执行即可。 
### Android
```bash
adb push libtal.so /data/local/tmp/.
adb shell "su -c 'cp /data/local/tmp/libtal.so /data/data/com.taobao.taobao/libtal.so'"
adb shell "su -c 'chmod 777 /data/data/com.taobao.taobao/libtal.so'"
```
安卓平台需使用`cli_trace_android.py`和`trace_input_android.js`，由于案例过于敏感，本处不做过多解释。 



### 关于附件说明
测试使用 `浙江省网安省赛赛题 - Warning` , `N1CTF Junior 2025 - TrueOperator` 以及 `强网杯2025 - ark_js_vm` 进行测试，侵联则删。 
## 开源许可证
本仓库的二进制静态链接自多个第三方库，并在遵循各个开源协议的前提下进行分发。 

详细可见本项目附件 [COPYING](COPYING)