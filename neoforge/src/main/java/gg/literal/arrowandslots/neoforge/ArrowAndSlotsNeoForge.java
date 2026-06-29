package gg.literal.arrowandslots.neoforge;

import gg.literal.arrowandslots.ArrowAndSlots;
import gg.literal.arrowandslots.ArrowSlotHelper;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.living.LivingGetProjectileEvent;

@Mod(ArrowAndSlots.MOD_ID)
public class ArrowAndSlotsNeoForge {
    public ArrowAndSlotsNeoForge(IEventBus modEventBus) {
        ArrowAndSlots.init();
        NeoForge.EVENT_BUS.addListener(this::onGetProjectile);
    }

    private void onGetProjectile(LivingGetProjectileEvent event) {
        if (event.getEntity() instanceof Player player) {
            ItemStack weapon = event.getProjectileWeaponItemStack();
            ItemStack arrow = ArrowSlotHelper.findArrowAbove(player, weapon);
            if (arrow != null) {
                event.setProjectileItemStack(arrow);
            }
        }
    }
}