#![no_std]
#![no_main]

mod memory;
mod scheduler;
mod syscalls;
mod ipc;
mod isolation;
mod temporal;

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
fn main() {}
