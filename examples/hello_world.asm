.orig 0x3000

; Programm:
lea r0, MyText
PUTS
HALT

; Data:
MyText: .stringz "Hello, world!"

.end
