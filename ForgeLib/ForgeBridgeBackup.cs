//using ForgeLib.Halo3;
//using RGiesecke.DllExport;
//using System;
//using System.Collections.Generic;
//using System.Diagnostics;
//using System.Runtime.InteropServices;
//using System.Linq;

//namespace ForgeLib
//{


//    public enum Game : byte
//    {
//        None,
//        HaloReach,
//        Halo3,
//    }

//    public enum Map
//    {
//        None,

//        // Halo Reach
//        // TODO: Attribute strings
//        Boardwalk,    //50_panopticon
//        Boneyard,     //70_boneyard
//        Countdown,    //45_launch_station
//        Powerhouse,   //30_settlement
//        Reflection,   //52_ivory_tower
//        Spire,        //35_island
//        Sword_Base,   //20_sword_slayer
//        Zealot,       //45_aftship
//        Anchor_9,     //dlc_slayer
//        Breakpoint,   //dlc_invasion
//        Tempest,      //dlc_medium
//        Condemned,    //condemned
//        Highlands,    //trainingpreserve
//        Battle_Canyon,//cex_beavercreek
//        Penance,      //cex_damnation
//        Ridgeline,    //cex_timberland
//        Solitary,     //cex_prisoner
//        High_Noon,    //cex_hangemhigh
//        Breakneck,    //cex_headlong
//        Forge_World,   //forge_halo

//        // Halo 3
//        Construct,
//        Epitaph,
//        Guardian,
//        HighGround,
//        Isolation,
//        LastResort,
//        Narrows,
//        Sandtrap,
//        Snowbound,
//        ThePit,
//        Valhalla,
//        Foundry,
//        RatsNest,
//        Standoff,
//        Avalanche,
//        Blackout,
//        GhostTown,
//        ColdStorage,
//        Assembly,
//        Orbital,
//        Sandbox,
//        Citadel,
//        Heretic,
//        Longshore
//    }


//    public static class ForgeBridge
//    {
//        public const int H3_maxObjects = 640;
//        public static Game currentGame;
//        public static ProcessMemory memory = new ProcessMemory();
//        public static Map currentMap;
//        public static Dictionary<int, MccForgeObject> forgeObjects = new Dictionary<int, MccForgeObject>();
//        static UIntPtr objectPtr;
//        static UIntPtr objectCount;
//        static UIntPtr ptrAddress;

//        static H3_MapVariant h3_mvar = new H3_MapVariant();

//        static TestH3_MapVariant nutMvar = new TestH3_MapVariant();

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static int GetDllVersion() => 4;

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static bool TrySetConnect(bool connect)
//        {
//            if (connect)
//            {
//                if (memory.Connected) return true;

//                Process[] processes = null;
//                foreach (string procName in new string[] { "MCC-Win64-Shipping", "MCCWinStore-Win64-Shipping" })
//                {
//                    processes = Process.GetProcessesByName(procName);
//                    if (processes.Length > 0) goto FoundProcess;
//                }

//                lastError = "Failed to find Master Chief Collection process.";
//                return false;

//            FoundProcess:
//                if (!memory.OpenProcess(processes[0].Id))
//                {
//                    lastError += "Failed to connect to process.\n";
//                    return false;
//                }
//            }
//            else
//            {
//                try
//                {
//                    memory.CloseProcess();
//                }
//                catch
//                {
//                    lastError = "Failed to close process.";
//                    return false;
//                }
//            }

//            return true;
//        }

//        public static string lastError;
//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        [return: MarshalAs(UnmanagedType.LPWStr)]
//        public static string GetLastError() => lastError;

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static int GetObjectCount() => forgeObjects.Count;

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static unsafe H3_ForgeObject* GetObjectPtr(int i)
//        {
//            return MccForgeObject.GetPointer(i);
//        }

//        static void findPointer(UIntPtr halo3Base)
//        {
//            ptrAddress = halo3Base + 0x2B3EF98;
//            ulong max = 140737488355327;
//            ulong min = 140668768878592;

//            for (var i = 0; i < 180; i++)
//            {
//                UIntPtr addr = halo3Base + 0x2B3EF98;
//                foreach (int offset in new int[] { 0x8, 0x2B0, 0x1670, 0x20, 0x78 })
//                    addr = memory.ReadPointer(addr) + offset;

//                ulong casted = addr.ToUInt64();
//                if (casted < max && casted > min)
//                {
//                    ptrAddress = addr;
//                    objectPtr = ptrAddress + 0x1D8;
//                    objectCount = ptrAddress + 0xFC;
//                    var bytes = BitConverter.GetBytes(casted);
//                    Array.Reverse(bytes);
//                    Console.WriteLine("ADDRESS IS: ");
//                    Console.WriteLine(BitConverter.ToString(bytes).Replace("-", string.Empty));
//                    i = 181;
//                }
//            }
//        }


//        static void GetH3Pointer()
//        {

//            if (memory.TryGetModuleBaseAddress("halo3.dll", out UIntPtr halo3Base))
//            {

//                ptrAddress = halo3Base + 0x2B3EF98;
//                ulong max = 140737488355327;
//                ulong min = 140668768878592;

//                for (var i = 0; i < 180; i++)
//                {
//                    UIntPtr addr = halo3Base + 0x2B3EF98;
//                    foreach (int offset in new int[] { 0x8, 0x2B0, 0x1670, 0x20, 0x78 })
//                        addr = memory.ReadPointer(addr) + offset;

//                    ulong casted = addr.ToUInt64();
//                    if (casted < max && casted > min)
//                    {
//                        ptrAddress = addr;
//                        objectPtr = ptrAddress + 0x1D8;
//                        objectCount = ptrAddress + 0xFC;
//                        var bytes = BitConverter.GetBytes(casted);
//                        Array.Reverse(bytes);
//                        Console.WriteLine("ADDRESS IS: ");
//                        Console.WriteLine(BitConverter.ToString(bytes).Replace("-", string.Empty));
//                        i = 181;
//                    }
//                }

//                UIntPtr test = halo3Base + 0x2B3EF98;
//                if (ptrAddress != test)
//                {
//                    unsafe
//                    {
//                        fixed (H3_MapVariant* mvarPtr = &h3_mvar)
//                        {
//                            byte[] nut = new byte[64];
//                            if (memory.TryReadBytes(ptrAddress, nut, 64))
//                            {
//                                Console.WriteLine("In the GetH3Pointer func");
//                                Console.WriteLine(ToReadableByteArray(nut));
//                            }
//                            if (memory.TryReadStruct(ptrAddress, mvarPtr))
//                            {
//                                Console.WriteLine("BRIDGE LOGS");
//                                Console.WriteLine("====================\n");
//                                Console.WriteLine("Reading Halo 3 MVAR");
//                                Console.WriteLine(h3_mvar.data.DisplayName);
//                                Console.WriteLine(h3_mvar.data.Description);
//                                Console.WriteLine(h3_mvar.data.Author);
//                                Console.WriteLine("END BRIDGE LOGS\n");

//                                H3_ForgeObject* objPtr = h3_mvar.GetForgeObjects();
//                                for (int i = 0; i < 640; i++)
//                                {
//                                    H3_ForgeObject obj = *objPtr;
//                                    objPtr++;
//                                }
//                            }
//                            else
//                            {
//                                Console.WriteLine("Fail!");
//                            }
//                        }
//                    }
//                }
//            }
//        }

//        static void GetPointers()
//        {
//            if (memory.TryGetModuleBaseAddress("halo3.dll", out UIntPtr halo3Base))
//            {
//                findPointer(halo3Base);
//            }
//            else
//            {
//                currentGame = Game.None;
//            }
//        }

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static void ReadMemory()
//        {
//            GetH3Pointer();
//            //GetPointers();
//        }

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static void WriteMemory(string hex, int index)
//        {
//            if (!memory.Connected) return;
//            byte[] outArr = StringToByteArray(hex);
//            UIntPtr ptr = objectPtr + (index * H3_ForgeObject.size);
//            memory.TryWriteBytes(ptr, outArr);

//        }

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static void WriteCount(short count)
//        {
//            if (!memory.Connected) return;
//            byte[] countArray = BitConverter.GetBytes(count);
//            memory.TryWriteBytes(objectCount, countArray);

//        }

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static void ClearObjectList() => forgeObjects.Clear();


//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static unsafe H3_MapVariant* GetH3_MVAR_Ptr()
//        {
//            h3_mvar = default;
//            GetH3Pointer();
//            //GetPointers();
//            fixed (H3_MapVariant* ptr = &h3_mvar) return ptr;
//        }

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static Game GetGame() => currentGame;

//        [DllExport(CallingConvention = CallingConvention.Cdecl)]
//        public static H3_MapVariant GetH3_MVAR() => h3_mvar;

//        static public string ToReadableByteArray(byte[] bytes)
//        {
//            return string.Join(", ", bytes);
//        }

//        public static byte[] StringToByteArray(string hexString)
//        {
//            return Enumerable.Range(0, hexString.Length)
//                             .Where(x => x % 2 == 0)
//                             .Select(x => Convert.ToByte(hexString.Substring(x, 2), 16))
//                             .ToArray();
//        }

//    }
//}
