package gg.literal.arrowandslots.fabric;

import gg.literal.arrowandslots.ArrowAndSlots;
import net.fabricmc.api.ModInitializer;

public class ArrowAndSlotsFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        ArrowAndSlots.init();
    }
}