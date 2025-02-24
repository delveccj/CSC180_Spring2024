
# **Lab: Buffer Overflows & Debugging in Linux (ARM64)**
### **Objective:**  
1️⃣ **Run the program normally (no crash).**  
2️⃣ **Cause a segmentation fault using buffer overflow.**  
3️⃣ **Analyze the crash in GDB.**  
4️⃣ **Understand how return addresses can be corrupted.**  

Note, your professor worked with ChatGPT to make this lab work!

---

## **🛠 Step 1: Set Up the Vulnerable Program**
### **Create the file (`overflow.c`)**

```bash
nano overflow.c
```

Paste this vulnerable C code:

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

Save the file!

---

## **🛠 Step 2: Compile the Program (Disable Protections)**

```bash
gcc -o overflow overflow.c -fno-stack-protector -z execstack -g
```

### **What This Does:**
- `-fno-stack-protector` → Disables stack canaries (stack protection).  
- `-z execstack` → Allows execution on the stack.  
- `-g` → Includes debug symbols for GDB analysis.  

---

## **🛠 Step 3: Run the Program Normally (No Crash)**
Try with a normal input:

```bash
./overflow hello
```

✅ Expected output:

```
You entered: hello
```

✅ No crash! The buffer safely holds `"hello"`.

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
This means we **overwrote something critical in memory**.

---

Absolutely! Here's the **updated GDB section**, explaining everything step by step.  

---

# **🛠 Step 5: Analyze the Crash in GDB**  
Now that we **crashed the program**, let’s investigate what happened using **GDB (GNU Debugger)**.  

## 🔍 **What Is GDB?**  
GDB allows us to:  
✅ **Run the program step by step** and pause execution.  
✅ **Inspect registers, memory, and stack contents** in real time.  
✅ **Identify crashes and find vulnerabilities.**  

---

## **🛠 Step 6: Set a Breakpoint on the Vulnerable Function**  
We first run GDB and pause execution **before the overflow happens**.  

### **1️⃣ Start GDB on Our Program**
Run:  
```bash
gdb -q ./overflow
```
🔹 `-q` starts GDB **without the banner clutter**.  

### **2️⃣ Set a Breakpoint at `vulnerable_function`**  
A **breakpoint** stops the program before a specific function executes.  
In GDB, type:  
```gdb
break vulnerable_function
```
You should see:  
```
Breakpoint 1 at 0xaaaaaaaa07d0: file overflow.c, line 5.
```
This means GDB will **pause execution when `vulnerable_function` starts**.

---

## **🛠 Step 7: Run the Program with Normal Input**  
Now, run the program with **safe input** (`hello`):  
```gdb
run hello
```
💥 The program **pauses** at `vulnerable_function`.  

### **3️⃣ Check the Registers (Before Overflow)**
At the breakpoint, check register values:  
```gdb
info registers
```
You should see:
```
x30 = 0xaaaaaaaa0858
```
✅ **`x30` (Link Register) is clean!** It holds the correct **return address** (`0xaaaaaaaa0858`), meaning no corruption has occurred.

### **4️⃣ Inspect the Stack (Before Overflow)**
Let's look at **10 entries** in memory from the **stack pointer (`sp`)**:  
```gdb
x/10gx $sp
```
You’ll see normal stack values, including the **return address** in memory.  
✅ The stack is **unchanged and safe** at this point.

Now, let’s **continue execution normally**:  
```gdb
continue
```
✅ The program prints `"You entered: hello"` and exits **without crashing**.

---

# **🛠 Step 8: Run the Program with an Overflow (Crash Time!)**  
Now, we trigger the **buffer overflow** and watch the destruction!  

```gdb
run AAAAAAAAAAAAAAAAAAAAA
```
💥 **Boom! Segmentation fault!**  
The program **crashes**, but GDB catches it.

---

# **🛠 Step 9: Inspect the Damage**  
Now, let's see what changed!  

### **1️⃣ Check Registers (Something’s Wrong!)**  
Run:
```gdb
info registers
```
🔍 Look at **`x30` (return address)**. It might now be:
```
x30 = 0x4141414141414141
```
🔥 **`0x4141414141414141` is just "AAAAAAA..." in ASCII!**  
✅ This means **our input overwrote the return address!** YIKES! 😲  

### **2️⃣ Look at the Stack (Corruption Confirmed!)**  
Now, inspect the stack memory again:
```gdb
x/10gx $sp
```
🔍 You should **see our "AAAAAA..." input** written into the stack, replacing the old return address.

✅ **We completely overwrote the return address with user-controlled input!**  
**If we replace it with a valid function address, we can hijack execution!** 🚀

---

# 🎯 **Key Takeaways**
✅ **Before the overflow**, `x30` (return address) is intact.  
✅ **After the overflow**, `x30` is replaced with `"AAAA..."` (our input).  
✅ **The stack memory shows our exploit in action.**  
✅ **This is the foundation of many real-world exploits!**  

🚀 Want to **redirect execution somewhere fun**? Let's hijack it to call `system("/bin/sh")` next! 😏🔥