extern getline
extern free
extern strlen
extern strncmp
extern stdin
extern exit
extern printf

section .text
global _start
    

func1:
    mov rbx, rsi;
    mov rcx, rdi;

    mov rdi, rbx;
    call strlen;
    mov rcx, rax;

    cmp rcx, 27;
    jne mmmh;
    
    mov rdi, rbx;
    mov rsi, hackademint;
    mov rdx, hackalen;
    
    call strncmp;
    
    cmp rax, 0;
    jne mmmh;

    cmp BYTE [rbx+25], 0x7d;   
    ja mmmh;
    jb mmmh;


    mov rax, 0;
    ret;

mmmh:
    mov rax, -1;
    ret;

func2:

    mov rdx, QWORD [rbx];
    mov rax, 0x1122334455667788;
    xor rdx, rax;
    mov rsi, 0x427d40750a2b04c9;
    cmp rdx, rsi;
    jne mmmh;

    add rbx, 8;
    xor rcx, rcx;
    mov ecx, DWORD [rbx];

    mov rbp, 1;
    xor rsi, rsi;

    shl rbp, 2;
    add rsi, rbp;

    shl rbp, 2;
    add rsi, rbp;

    shl rbp, 1;
    add rsi, rbp;

    shl rbp, 1;
    add rsi, rbp;

    shl rbp, 3;
    add rsi, rbp;

    shl rbp, 3;
    add rsi, rbp;

    shl rbp, 1;
    add rsi, rbp;

    shl rbp, 1;
    add rsi, rbp;

    shl rbp, 6;
    add rsi, rbp;

    shl rbp, 1;
    add rsi, rbp;

    shl rbp, 4;
    add rsi, rbp;

    shl rbp, 1;
    add rsi, rbp;

    shl rbp, 1;
    add rsi, rbp;

    shl rbp, 2;
    add rsi, rbp;

    shl rbp, 1;
    add rsi, rbp;

    cmp rcx, rsi;
    jne mmmh;

    add rbx, 4;

    cmp BYTE [rbx], 0x47;
    jne mmmh;

    xor rax, rax
    ret;

_start:
    push 0;
    mov rdi, rsp;
    push 0;
    xor rsi, rsi;
    xor rsi, rsp;

    push rsi;
    push rdi;    

    mov rdx, stdin;
    mov rdx, QWORD [rdx];

    call getline;

    pop rdi;
    pop rsi;

    mov rsi, QWORD [rdi];
    lea rdi, QWORD [rdi-8];
    mov rdi, QWORD [rdi];

    call func1;
    cmp rax, -1;
    je bye;

    add rbx, hackalen;
    call func2;
    cmp rax, -1;
    je bye;

    sub rbx, 24;
    mov rdi, gg;
    mov rsi, rbx;
    call printf
    call exit;



bye:

    mov rdi, nope;
    call printf;
    call exit;

section .data
    hackademint db "HackademINT{"
    hackalen equ $-hackademint
    db 0
    nope db "Nope :(", 0
    gg db "You can validate with this flag : %s", 0







