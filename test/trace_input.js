

let linux_path = "/mnt/d/qbdi/Release/linux/libtal.so";
let android_path = "/data/data/com.taobao.taobao/libtal.so";
let windows_path = "D:\\qbdi\\cmake-build-visualstudio\\tal.dll";

let target = "Warning"

function add_escape(m, break_addr, return_addr) {
    let add_escape = new NativeFunction(m.findExportByName("add_escape"), "void", ["pointer", "pointer"])
    add_escape(break_addr, return_addr)
}

function add_resume(m,return_addr) {
    let add_resume = new NativeFunction(m.findExportByName("add_resume"), "void", ["pointer"])
    add_resume(return_addr)
}
function trace(m, addr, end, printMode) {
    if (!m) {
        console.error("load so fail")
        return
    }
    let trace_function = new NativeFunction(m.findExportByName("trace"), "void", ["pointer", "pointer", "int", "int"])
    let set_log_path_function = new NativeFunction(m.findExportByName("set_log_path"), "void", ["pointer"])
    let remove_range_function = new NativeFunction(m.findExportByName("remove_range"), "void", ["pointer", "pointer"])
    trace_function(addr, ptr(end), 1, printMode)
    var path = Memory.alloc(0x420);
    path.writeUtf8String("linux/")
    set_log_path_function(path)
}


function sleep(s) {
    let start = new Date().getTime();
    while (new Date().getTime() - start < 1000 * s) { }
}



function start_trace(mod) {

    let addr4 = mod.base.add(0x010C3)
    console.log("" + addr4);
    console.log(Instruction.parse(addr4).toString());
    let listen = Interceptor.attach(addr4, {
        onEnter: function (args) {
            listen.detach()
            console.log("init hooked setting trace")
            sleep(1)
            let lib_name = Process.platform === "windows" ? "tal.dll" : "libtal.so"
            // console.log("ttd_name:", Process.enumerateModules().map(m => m.name))
            let tal = Process.findModuleByName(lib_name)
            trace(tal, mod.base.add(0x1120), 0, 4)
            set_taint_str(tal, "1111111111111111111111111111111111111111")
        }
    })

}


let mod = Process.findModuleByName(target)
console.log("target:", mod.base)
start_trace(mod)


if (Process.platform === "linux") {
    Module.load(linux_path)
} else if (Process.platform === "windows") {
    Module.load(windows_path)
} else if (Process.platform === "android") {
    Module.load(android_path)
}