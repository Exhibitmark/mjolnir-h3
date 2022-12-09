using System;
using System.Runtime.InteropServices;

namespace ForgeLib {
    public class MccForgeObject {
        static unsafe ForgeObject* objects;
        static unsafe MccForgeObject() {
            objects = (ForgeObject*)Marshal.AllocHGlobal(Marshal.SizeOf(typeof(ForgeObject)) * ForgeBridge.maxObjects).ToPointer();
        }

        public static unsafe ForgeObject* GetPointer(int i) => objects + (i % ForgeBridge.maxObjects);


        public UIntPtr mccPointer;
        public unsafe ForgeObject* data;

        public MccForgeObject(UIntPtr mccPointer, int i) {
            this.mccPointer = mccPointer;

            unsafe {
                data = GetPointer(i);
            }
        }

        public void ReadFromMemory() {
            unsafe {
                ForgeBridge.memory.TryReadStruct(mccPointer, data);
            }
        }

        public void WriteMemory() {
            unsafe {
                ForgeBridge.memory.TryWriteStruct(mccPointer, data);
            }
        }

        public override string ToString() {
            unsafe {
                return data->ToString();
            }
        }
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct Transform {
        public float3 position;
        public float3 forward;
        public float3 up;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct ShapeData {
        public float width;
        public float length;
        public float top;
        public float bottom;
    }

    [StructLayout(LayoutKind.Sequential, Pack = 1, Size = size)]
    public struct ForgeObject {
        public const int size = 76;

        public ushort show;
        public ushort itemCategory;
        public uint idExt;//0xFFFFFFFF
        public Transform transform;
        public ushort spawnRelativeToMapIndex;//0xFFFF
        public byte itemVariant;
        public byte pad1;

        public ShapeData shapeDims;
        public Shape shape;

        public byte spawnSequence;
        public byte spawnTime;
        public byte cachedType;
        public ushort gtLabelIndex;
        public Flags flags;
        public Color team;
        public TypeSpecificInfo otherInfo;
        public Color color;
        public byte pad2;

        public enum Shape : byte { None, Cylinder = 2, Box }
        public enum Flags : byte {
            PhysicsNormal = 0b00000000,
            PhysicsFixed  = 0b01000000,
            PhysicsPhased = 0b11000000,
            PhysicsMask   = 0b11000000,
            GameSpecific  = 0b00100000,
            Asymmetric    = 0b00001000,
            Symmetric     = 0b00000100,
            SymmetryMask  = 0b00001100,
            HideAtStart   = 0b00000010
        }
        public enum Color : byte { Red, Blue, Green, Orange, Purple, Yellow, Brown, Pink, Neutral, TeamColor = 255 }

        [StructLayout(LayoutKind.Explicit, Size = 2)]
        public struct TypeSpecificInfo {// based on cachedType
            [FieldOffset(0)] public byte spareClips;

            [FieldOffset(0)] public byte teleporterChannel;//0-25
            [FieldOffset(1)] public TeleFlags teleporterPassability;

            [FieldOffset(0)] public byte locationNameIndex;

            public enum TeleFlags : byte {
                NoPlayers = 0b00000001,
                LandVehicles = 0b00000010,
                HeavyVehicles = 0b00000100,
                FlyingVehicles = 0b00001000,
                Projectiles = 0b00010000
            }
        }

        /*cachedType
	        0: props, weapons, respawns, flag stands, hill markers, uncached things, everything...?
	        1: guns, some initial spawns(???)
	        2: grenades
	        7: light vehicles (ghost, mongoose, wart, rev, shade turret)
	        8: heavy vehicles
	        9: flying
	        12: 2 way tele
	        13: sender
	        14: reciever
	        15: initial spawn/respawns
	        16: flag/respawn zones
	        25: soft safe
	        26: kill boundary, some respawn
	        27: init loadout camera
        scriptLabelIndex// gameTypeLabel(?)
	        65535: objs, respawn
	        0: init spawn
	        1: flag stand
	        2: hill marker
	        3: capture plate*/

        public int Type => itemCategory << 8 | itemVariant;
        public string ItemName {
            get {
                if (ItemParser.TryTypeToName(Type, ForgeBridge.currentMap, out string name)) return name;
                return $"Unknown (0x{Type:X})";
            }
        }

        public override string ToString() => $"{ItemName} {position}";
    }
}
