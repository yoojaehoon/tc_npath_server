namespace py tcnpathmonitor

enum RETURN_CODE{
    RC_SUCCESS,
    RC_FAIL,
    RC_SERVER_NOT_FOUND,
    RC_SERVER_ALREADY_EXIST
}

struct OP_RESULT{
    1: RETURN_CODE rcode,
    2: string reason,
}

struct HardwareSpec {
    1: string flavor,
    2: i32 cpu_core,
    3: i32 memory_count,
    4: i32 memory_volume,
    5: i32 disk_count,
    6: i32 disk_volume
}

struct VmInfo {
    1: string hostname,
    2: string uuid,
    3: string availability_zone,
    4: string project_type,
    5: string nic1,
    6: string nic2,
}

struct AliveInfo {
    1: bool wmi_private_fx,
    2: bool wmi_private_fl,
    3: bool wmi_public_fx,
    4: bool wmi_public_fl,
    5: bool normal_public_fx,
    6: bool normal_public_fl,
    7: double wmi_private_fx_latency,
    8: double wmi_private_fl_latency,
    9: double wmi_public_fx_latency,
    10: double wmi_public_fl_latency,
    11: double normal_public_fx_latency,
    12: double normal_public_fl_latency
}

exception InvalidOperation {
    1: i32 whatOp,
    2: string why
}

service ServerSvc {
            OP_RESULT   reportAlive(1:string uuid, 2:AliveInfo aliveinfo),
            OP_RESULT   registVm(1:VmInfo vminfo),
    oneway  void        ping(),
}
