#![cfg_attr(not(test), no_std)]
#![cfg_attr(not(test), no_main)]

pub mod memory;
pub mod scheduler;
pub mod syscalls;
pub mod ipc;
pub mod isolation;
pub mod temporal;
pub mod axiarchy;

use core::panic::PanicInfo;

#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn _start() -> ! {
    // ARKHE OS Entry Point
    loop {}
}

#[cfg(not(test))]
#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}

#[cfg(test)]
pub fn main() {}
