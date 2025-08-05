from Lib.Debugger import info, warning, error
import os

def handle_response(self, text: str) -> str:
    if self.key:
        response = self.get_response(text)

        commands: str = response.split("commands<")[1].strip()[:-1].split(";")
        response: str = response.split("commands<")[0].strip()

        for command in commands:
            print("running command:", command)
            command = command.strip()
            if not command:
                continue

            if command == "quit":
                print(response)

                info("Closing the app...")
                return

            try:
                self.execute(command)
            except Exception as e:
                error(f"Errore comando '{command}': {e}")
        
        print(response)
        return
    
    print("AI is disabled")

def get_response(self, text: str) -> str:
    exploit_commands = ""
    if self.exploit and self.exploit.commands:
        exploit_commands = '\n'.join(
            f"{k:<12} {v}" for k, v in sorted(self.exploit.commands.items())
        )
        
    system_prompt = f"""
If you're asked to use an exploit, use this format:
use [exploit name]
  Example:
    use NoticedCloud/NCEXP
If you're asked to choose a payload, reply with "set payload (payload name)"
If you're asked to set a port, reply with "set lport (port)"
If you're asked to set an IP, reply with "set lhost (ip)"
If you're asked to show options, payloads, or exploits, reply with "show (options, payloads, or exploits)"
If you're asked to show the current directory, reply with "getcwd"
If you're asked to change the directory, reply with "cd (folder)"
If you're asked to show the available commands, reply with "help"
{exploit_commands}
If you're asked to run multiple commands at once, reply with "command1; command2; etc..."
Don't add anything after the command unless the user explicitly tells you.
Don't run the command unless told.

You are an assistant that executes terminal-like commands. Every time the user asks you to do something:

1. First, reply with a natural sentence like "Done, I've loaded the exploit." or "I couldn't find that command."
2. Then, in a new line, write the exact command(s) inside this tag format:
commands<(exact command here dont put the parentesis)>

⚠️ IMPORTANT:
- You must ALWAYS use the format: commands<...>
- If no command was requested or you don't understand, return: commands<>
- Never add explanations after commands<...
- Do not forget the "commands<...>" part, even if the user doesn't ask for it.
"""
    response = self.client.chat.completions.create(
        model=os.getenv("model"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        stream=False
    )


    return response.choices[0].message.content
