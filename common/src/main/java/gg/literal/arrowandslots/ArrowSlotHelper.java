package gg.literal.arrowandslots;

import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArrowItem;
import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;

public final class ArrowSlotHelper {
    private ArrowSlotHelper() {}

    @Nullable
    public static ItemStack findArrowAbove(Player player) {
        ItemStack mainHand = player.getMainHandItem();
        if (!(mainHand.getItem() instanceof BowItem)) return null;

        Inventory inv = player.getInventory();
        int selected = inv.selected;
        int aboveSlot = selected + 9;
        if (aboveSlot >= inv.getContainerSize()) return null;

        ItemStack above = inv.getItem(aboveSlot);
        if (above.isEmpty() || !(above.getItem() instanceof ArrowItem)) return null;

        return above;
    }
}