
; boot/bootloader_arm64.asm
.global _start

_start:
    /* Carregar kernel ELF do IPFS (CID fixo no setor 1) */
    /* Verificar assinatura Ed25519 (syscall 0x989) */
    /* Configurar páginação (4-level paging) */
    /* Saltar para o entry point do kernel */
    b kmain
