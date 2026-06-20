

const target = "libsgmainso-6.8.260404.so";
const taintStr = "1111111111111111111111111111111111111111";
const traceOffset = 0xCB4B8;
const logPath = "/data/data/com.taobao.taobao/";

const PrintMode = { ADDR: 0, BIN: 1, DEBUG: 2, TRACE: 3, TRITON: 4, TRACE_ARGS: 5, };
let talPath = {
    linux: "/mnt/d/qbdi/Release/linux/libtal.so",
    windows: "D:\\qbdi\\Release\\windows\\tal.dll",
}[Process.platform];


if(Process.arch=="arm64"){
    talPath = "/data/data/com.taobao.taobao/libtal.so"
}
const cstr = Memory.allocUtf8String;
const tal = Module.load(talPath);
let interval = setInterval(() => {

    const mod = Process.findModuleByName(target);
    if (mod) {
        clearInterval(interval);
    } else {
        return;
    }
    console.log(Process.platform);
    

    const exp = (name, ret, args) =>
        new NativeFunction(tal.findExportByName(name), ret, args);

    const setLogPath = exp("set_log_path", "void", ["pointer"]);
    const setTaintStr = exp("set_taint_str", "int", ["pointer"]);
    const trace = exp("trace", "void", ["pointer", "pointer", "int", "int"]);
    const addEscape = exp("add_escape", "void", ["pointer", "pointer"]);
    const addResume = exp("add_resume", "void", ["pointer"]);
    const setFunctionPrint = exp("set_function_print", "void", ["int", "int"]);
    console.log("[+] target:", mod.base);


    trace(mod.base.add(traceOffset), ptr(0), 1, PrintMode.TRACE_ARGS);
    setLogPath(cstr(logPath));
    setTaintStr(cstr(taintStr));

    send("script_ready");
}, 1);
