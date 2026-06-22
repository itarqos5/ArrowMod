package gg.literal.arrowandslots.neoforge;

import gg.literal.arrowandslots.ArrowAndSlots;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(ArrowAndSlots.MOD_ID)
public class ArrowAndSlotsNeoForge {
    public ArrowAndSlotsNeoForge(IEventBus modEventBus) {
        ArrowAndSlots.init();
    }
}