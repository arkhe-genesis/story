// kernel/src/syscalls.rs
#[repr(usize)]
pub enum Syscall {
    AnchorProof = 0x923,
    VerifyHumanity = 0x989,
    Infer100T = 0x9893,
    BinduMemory = 0x952,
    MeshRoute = 0x972,
    KyberEncrypt = 0x955,
    IpfsPin = 0x9721,
    NostrPublish = 0x973,
    TorRoute = 0x974,
    KernelIsolate = 0x9892,
    Evolve = 0x986,
    SelfHeal = 0x985,
    FairMetrics = 0x9895,
    ThesisGet = 0x965,
    AxiarchyVerify = 0x954,
}

// Trampolim da syscall
#[no_mangle]
pub extern "C" fn syscall_handler(
    syscall_num: usize,
    arg1: usize,
    arg2: usize,
    arg3: usize,
) -> usize {
    match syscall_num {
        // AnchorProof: arg1 = cid_ptr, arg2 = seal_ptr, arg3 = len
        x if x == Syscall::AnchorProof as usize => {
            crate::temporal::anchor(arg1, arg2, arg3)
        }
        // ThesisGet: arg1 = pid
        x if x == Syscall::ThesisGet as usize => {
            crate::scheduler::get_theosis(arg1 as u32)
        }
        // AxiarchyVerify: arg1 = code_hash_ptr
        x if x == Syscall::AxiarchyVerify as usize => {
            crate::axiarchy::verify_code(arg1)
        }
        // ... implementar as demais syscalls ...
        _ => 0,
    }
}
