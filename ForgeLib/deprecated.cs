using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ForgeLib
{
    class deprecated
    {
        /*
        static UIntPtr forgeObjectArrayPointer;
        static void GetForgeObjects()
        {
            // TODO: read as one byte array (maxObjects * ForgeObject.size bytes)
            // TODO: less allocatey system that preallocates all MccForgeObjects
            for (int i = 0; i < H3_maxObjects; i++)
            {
                UIntPtr objPtr = forgeObjectArrayPointer + i * H3_ForgeObject.size;
                byte flag = memory.ReadByte(objPtr);
                bool isObject = flag == 1;

                if (flag > 1)
                {
                    lastError += "\nUnknown flag!";
                    throw new Exception(lastError);
                }

                if (isObject)
                {
                    if (!forgeObjects.TryGetValue(i, out MccForgeObject fobj))
                    {
                        fobj = new MccForgeObject(objPtr, i);
                        forgeObjects[i] = fobj;
                    }

                    fobj.ReadFromMemory();
                }
                else
                {
                    if (forgeObjects.TryGetValue(i, out MccForgeObject fobj))
                    {
                        fobj.ReadFromMemory();
                        forgeObjects.Remove(i);
                    }
                }
            }
        }

        public static Game currentGame;
        [DllExport(CallingConvention = CallingConvention.Cdecl)]
        public static Game GetGame() => currentGame;

        [DllExport(CallingConvention = CallingConvention.Cdecl)]
        public static int ItemNameToType([MarshalAs(UnmanagedType.LPWStr)] string itemName)
        {
            if (ItemParser.TryNameToType(itemName, currentMap, out int type)) return type;
            return 0;
        }

        
        static void findPointer(UIntPtr halo3Base)
        {
            ptrAddress = halo3Base + 0x2B3EF98;
            ulong max = 140737488355327;
            ulong min = 140668768878592;

            for (var i = 0; i < 180; i++)
            {
                UIntPtr addr = halo3Base + 0x2B3EF98;
                foreach (int offset in new int[] { 0x8, 0x2B0, 0x1670, 0x20, 0x78 })
                    addr = memory.ReadPointer(addr) + offset;

                ulong casted = addr.ToUInt64();
                if (casted < max && casted > min)
                {
                    ptrAddress = addr;
                    objectPtr = ptrAddress + 0x1D8;
                    objectCount = ptrAddress + 0xFC;
                    var bytes = BitConverter.GetBytes(casted);
                    Array.Reverse(bytes);
                    Console.WriteLine("ADDRESS IS: ");
                    Console.WriteLine(BitConverter.ToString(bytes).Replace("-", string.Empty));
                    i = 181;
                }
            }
        }

        */

        //[DllExport(CallingConvention = CallingConvention.Cdecl)]
        //public static unsafe void AddObject(int i)
        //{
        //    //i is the object index of the 640. This is sent from Blender
        //    if (i >= H3_maxObjects) return;
        //    // I set forgeObjectArrayPointer to be the starting address of the forge objects in the map variant structure (Don't know if this is correct)
        //    /*
        //        UIntPtr addr = halo3Base + 0x1F89980;
        //        foreach (int offset in new int[] { 0x760, 0x368, 0xA00 })
        //            addr = memory.ReadPointer(addr) + offset;
        //        forgeObjectArrayPointer = addr + 0x1D8; 
        //        */
        //    // We get a pointer that is forgeObjectArrayPointer + (object_index * 84) so the start of the object in memory
        //    UIntPtr objPtr = forgeObjectArrayPointer + i * H3_ForgeObject.size;

        //    // New 
        //    MccForgeObject mccFobj = new MccForgeObject(objPtr, i);
        //    Console.WriteLine(mccFobj.data->transform);
        //    mccFobj.data->object_index = -1;
        //    mccFobj.data->helper_index = -1;
        //    forgeObjects[i] = mccFobj;
        //}

        //static void test()
        //{

        //    Process[] processes = Process.GetProcessesByName("MCC-Win64-Shipping");
        //    if (memory.TryGetModuleBaseAddress("halo3.dll", out UIntPtr halo3Base))
        //    {

        //        ptrAddress = halo3Base + 0x2B3EF98;
        //        ulong max = 140737488355327;
        //        ulong min = 140668768878592;

        //        for (var i = 0; i < 180; i++)
        //        {
        //            UIntPtr addr = halo3Base + 0x2B3EF98;
        //            foreach (int offset in new int[] { 0x8, 0x2B0, 0x1670, 0x20, 0x78 })
        //                addr = memory.ReadPointer(addr) + offset;

        //            ulong casted = addr.ToUInt64();
        //            if (casted < max && casted > min)
        //            {
        //                ptrAddress = addr;
        //                objectPtr = ptrAddress + 0x1D8;
        //                objectCount = ptrAddress + 0xFC;
        //                var bytes = BitConverter.GetBytes(casted);
        //                Array.Reverse(bytes);
        //                Console.WriteLine("ADDRESS IS: ");
        //                Console.WriteLine(BitConverter.ToString(bytes).Replace("-", string.Empty));
        //                i = 181;
        //            }
        //        }

        //        UIntPtr test = halo3Base + 0x2B3EF98;
        //        if (ptrAddress != test)
        //        {
        //            unsafe
        //            {
        //                fixed (H3_MapVariant* mvarPtr = &h3_mvar)
        //                {
        //                    byte[] nut = new byte[64];
        //                    if (memory.TryReadBytes(ptrAddress, nut, 64))
        //                    {
        //                        Console.WriteLine("In the GetH3Pointer func");
        //                        Console.WriteLine(ToReadableByteArray(nut));
        //                    }
        //                    if (memory.TryReadStruct(ptrAddress, mvarPtr))
        //                    {
        //                        Console.WriteLine("BRIDGE LOGS");
        //                        Console.WriteLine("====================\n");
        //                        Console.WriteLine("Reading Halo 3 MVAR");
        //                        Console.WriteLine(h3_mvar.data.DisplayName);
        //                        Console.WriteLine(h3_mvar.data.Description);
        //                        Console.WriteLine(h3_mvar.data.Author);
        //                        Console.WriteLine("END BRIDGE LOGS\n");

        //                        H3_ForgeObject* objPtr = h3_mvar.GetForgeObjects();
        //                        for (int i = 0; i < 640; i++)
        //                        {
        //                            H3_ForgeObject obj = *objPtr;
        //                            objPtr++;
        //                        }
        //                    }
        //                    else
        //                    {
        //                        Console.WriteLine("Fail!");
        //                    }
        //                }
        //            }
        //        }
        //    }
        //}


    }
}
