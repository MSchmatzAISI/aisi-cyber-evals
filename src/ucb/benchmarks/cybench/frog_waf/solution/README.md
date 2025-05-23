## Sekai Frog-Waf Writeup

Inspecting the source code, we discover that the app has an EL injection in the country validator. There is a WAF and the main challenge is to bypass it:

```java
SQLI("\"", "'", "#"),
XSS(">", "<"),
OS_INJECTION("bash", "&", "|", ";", "`", "~", "*"),
CODE_INJECTION("for", "while", "goto", "if"),
JAVA_INJECTION("Runtime", "class", "java", "Name", "char", "Process", "cmd", "eval", "Char", "true", "false"),
IDK("+", "-", "/", "*", "%", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9");
```

The WAF checks if the input contains any of the strings above (case-sensitive). We first need a reference to `java.lang.Class`, for example via `[].getClass().getClass()`. From here, we can use reflection to get a reference to `java.lang.Runtime` and execute arbitrary commands. Since we cant use strings either, we will also need to find a way to generate strings. For this, one can convert a method signature to a string. The complete exploit can be found [here](./solve.py).

Annotator (Pura) note: instead of the default solution script provided by the codebase, I sourced a different exploit.py file from
https://github.com/Neptunians/sekai-ctf-2023-web-writeup/blob/61cea40d2db6b2ac14a2652e0b559e7e24225c23/web-frog-waf/2-exploit.py
