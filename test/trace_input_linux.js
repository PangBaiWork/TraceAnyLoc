const target = "Warning";
const taintStr = "1111111111111111111111111111111111111111";
const traceOffset = 0x1120;
const logPath = "linux/";
const PrintMode = {ADDR: 0, BIN: 1, DEBUG: 2, TRACE: 3, TRITON: 4, TRACE_ARGS: 5,};

const talPath = {
    linux: "/sharedisk/qbdi/Debug/linux/libtal.so",
    // linux: "/mnt/d/qbdi/Release/linux/libtal.so",
    windows: "D:\\qbdi\\Release\\windows\\tal.dll",
    android: "/data/data/com.taobao.taobao/libtal.so",
}[Process.platform];

const cstr = Memory.allocUtf8String;

const mod = Process.getModuleByName(target);
const tal = Module.load(talPath);

const exp = (name, ret, args) =>
    new NativeFunction(tal.findExportByName(name), ret, args);

const setLogPath  = exp("set_log_path",  "void", ["pointer"]);
const setTaintStr = exp("set_taint_str", "int",  ["pointer"]);
const trace       = exp("trace",         "void", ["pointer", "pointer", "int", "int"]);
const addEscape   = exp("add_escape",    "void", ["pointer", "pointer"]);
const addResume   = exp("add_resume",    "void", ["pointer"]);
const setFunctionPrint = exp("set_function_print","void", ["int","int"]);
console.log("[+] target:", mod.base);


trace(mod.base.add(traceOffset), ptr(0), 1, PrintMode.TRACE_ARGS);
setLogPath(cstr(logPath));
setTaintStr(cstr(taintStr));

send("script_ready");
