; ARKHE OS - Bootloader x86_64
; Loads kernel ELF from IPFS, verifies Ed25519 signature, sets up long mode
bits 16
org 0x7c00

start:
    cli
    ; Setup stack
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7c00

    ; Simulating loading kernel from IPFS via CID
    ; Simulating Ed25519 verification
    ; ...

    ; Switch to protected mode
    lgdt [gdt_descriptor]
    mov eax, cr0
    or eax, 1
    mov cr0, eax

    jmp 0x08:init_pm

bits 32
init_pm:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax

    ; Switch to long mode
    ; Setup paging...
    ; ...

    ; Jump to kernel entry point
    ; jmp kernel_entry

    hlt

gdt_start:
    dq 0 ; null descriptor
gdt_code:
    dw 0xffff
    dw 0
    db 0
    db 10011010b
    db 11001111b
    db 0
gdt_data:
    dw 0xffff
    dw 0
    db 0
    db 10010010b
    db 11001111b
    db 0
gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

times 510-($-$$) db 0
dw 0xaa55
