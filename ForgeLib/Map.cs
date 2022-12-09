namespace ForgeLib {
    public static class MapUtil {
        public static Map FromIdString(string id) {
            switch (id) {
                default: return Map.None;
            }
        }

        public static Map FromH3_Enum(Halo3.Map map) => Map.Construct + (map - Halo3.Map.CONSTRUCT);

        public static string ToString(Map map) {
            switch (map) {
                case Map.None: return "None";
                default: return "Unknown";


                // Halo 3
                case Map.Construct: return "Construct";
                case Map.Epitaph: return "Epitaph";
                case Map.Guardian: return "Guardian";
                case Map.HighGround: return "High Ground";
                case Map.Isolation: return "Isolation";
                case Map.LastResort: return "Last Resort";
                case Map.Narrows: return "Narrows";
                case Map.Sandtrap: return "Sandtrap";
                case Map.Snowbound: return "Snowbound";
                case Map.ThePit: return "The Pit";
                case Map.Valhalla: return "Valhalla";
                case Map.Foundry: return "Foundry";
                case Map.RatsNest: return "Rats Nest";
                case Map.Standoff: return "Standoff";
                case Map.Avalanche: return "Avalanche";
                case Map.Blackout: return "Blackout";
                case Map.GhostTown: return "Ghost Town";
                case Map.ColdStorage: return "Cold Storage";
                case Map.Assembly: return "Assembly";
                case Map.Orbital: return "Orbital";
                case Map.Sandbox: return "Sandbox";
                case Map.Citadel: return "Citadel";
                case Map.Heretic: return "Heretic";
                case Map.Longshore: return "Longshore";
            }
        }
    }
}
