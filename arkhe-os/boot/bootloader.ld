/* ARKHE OS - Bootloader Linker Script */
ENTRY(start)

SECTIONS {
    . = 0x7c00;

    .text : {
        *(.text)
    }

    .data : {
        *(.data)
    }

    .bss : {
        *(.bss)
    }

    /DISCARD/ : {
        *(.eh_frame)
    }
}
