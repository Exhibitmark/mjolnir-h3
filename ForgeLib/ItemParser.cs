using System.Collections.Generic;

namespace ForgeLib {
    public static class ItemParser {
        public class TwoWayDictionary<T1, T2> {
            Dictionary<T1, T2> t1Tot2 = new Dictionary<T1, T2>();
            Dictionary<T2, T1> t2Tot1 = new Dictionary<T2, T1>();

            public T2 this[T1 key] {
                get => t1Tot2[key];
                set {
                    t1Tot2[key] = value;
                    t2Tot1[value] = key;
                }
            }
            public T1 this[T2 key] {
                get => t2Tot1[key];
                set {
                    t2Tot1[key] = value;
                    t1Tot2[value] = key;
                }
            }

            public bool TryGetValue(T1 key, out T2 value) => t1Tot2.TryGetValue(key, out value);
            public bool TryGetValue(T2 key, out T1 value) => t2Tot1.TryGetValue(key, out value);
        }

        static void AddNext<T>(this TwoWayDictionary<int, T> dict, ref int key, T value) {
            dict[key] = value;
            key = (key + (1 << 8)) & 0xFF00;
        }
        static void AddSubcategory<T>(this TwoWayDictionary<int, T> dict, ref int key, params T[] values) {
            foreach (T value in values)
                dict[key++] = value;
            key = (key + (1 << 8)) & 0xFF00;
        }

        static TwoWayDictionary<int, string> universalTypes = new TwoWayDictionary<int, string>();
        static Dictionary<Map, TwoWayDictionary<int, string>> maps = new Dictionary<Map, TwoWayDictionary<int, string>>();

        static ItemParser() {
            #region Universal
            #region Weapons Human
            int key = 0;
            universalTypes.AddNext(ref key, "Assault Rifle");
            universalTypes.AddNext(ref key, "DMR");
            universalTypes.AddNext(ref key, "Grenade Launcher");
            universalTypes.AddNext(ref key, "Magnum");
            universalTypes.AddNext(ref key, "Rocket Launcher");
            universalTypes.AddNext(ref key, "Shotgun");
            universalTypes.AddNext(ref key, "Sniper Rifle");
            universalTypes.AddNext(ref key, "Spartan Laser");
            universalTypes.AddNext(ref key, "Frag Grenade");
            universalTypes.AddNext(ref key, "Mounted Machinegun");
            #endregion
            #region Weapons Covenant
            universalTypes.AddNext(ref key, "Concussion Rifle");
            universalTypes.AddNext(ref key, "Energy Sword");
            universalTypes.AddNext(ref key, "Fuel Rod Gun");
            universalTypes.AddNext(ref key, "Gravity Hammer");
            universalTypes.AddNext(ref key, "Focus Rifle");
            universalTypes.AddNext(ref key, "Needle Rifle");
            universalTypes.AddNext(ref key, "Needler");
            universalTypes.AddNext(ref key, "Plasma Launcher");
            universalTypes.AddNext(ref key, "Plasma Pistol");
            universalTypes.AddNext(ref key, "Plasma Repeater");
            universalTypes.AddNext(ref key, "Plasma Rifle");
            universalTypes.AddNext(ref key, "Spiker");
            universalTypes.AddNext(ref key, "Plasma Grenade");
            universalTypes.AddNext(ref key, "Plasma Turret");
            #endregion
            #region Armor Abilities
            universalTypes.AddNext(ref key, "Active Camouflage");
            universalTypes.AddNext(ref key, "Armor Lock");
            universalTypes.AddNext(ref key, "Drop Shield");
            universalTypes.AddNext(ref key, "Evade");
            universalTypes.AddNext(ref key, "Hologram");
            universalTypes.AddNext(ref key, "Jet Pack");
            universalTypes.AddNext(ref key, "Sprint");
            #endregion
            #endregion

        }

        public static bool TryTypeToName(int type, Map map, out string name) {
            if (universalTypes.TryGetValue(type, out name)) return true;
            if (maps.TryGetValue(map, out TwoWayDictionary<int, string> mapTypes) && mapTypes.TryGetValue(type, out name)) return true;

            return false;
        }

        public static bool TryNameToType(string name, Map map, out int type) {
            if (universalTypes.TryGetValue(name, out type)) return true;
            if (maps.TryGetValue(map, out TwoWayDictionary<int, string> mapTypes) && mapTypes.TryGetValue(name, out type)) return true;

            return false;
        }
    }
}
