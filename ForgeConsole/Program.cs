using ForgeLib;
using ForgeLib.Halo3;
using System;
using System.Diagnostics;
using System.Linq;

namespace ForgeConsole
{

    class Program
    {

        static void Main(string[] args)
        {
            /*
            if (!ForgeBridge.TrySetConnect(true))
            {
                Console.WriteLine(ForgeBridge.GetLastError());
                return;
            }

            
            ForgeBridge.ReadMemory();

            Console.WriteLine($"{ForgeBridge.GetObjectCount()} Objects");

            unsafe
            {
                int c = ForgeBridge.GetObjectCount();
                for (int i = 0; i < c; i++)
                {
                    H3_ForgeObject fobj = *ForgeBridge.GetObjectPtr(i);
                }
            }

            */

            Process[] processes = Process.GetProcessesByName("MCC-Win64-Shipping");
            //int BaseAddress = processes[0].MainModule.BaseAddress.ToInt32();
            Console.WriteLine(processes[0].MainModule.BaseAddress);
            Console.Read();
        }
    }
}