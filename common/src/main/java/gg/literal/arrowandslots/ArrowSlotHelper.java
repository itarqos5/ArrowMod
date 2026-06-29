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
    public static ItemStack findArrowAbove(Player player, int bowSlot, ItemStack weaponStack) {
        try {
            if (weaponStack.isEmpty() || !(weaponStack.getItem() instanceof BowItem)) return null;

            Inventory inv = player.getInventory();
            if (bowSlot < 0 || bowSlot >= 9) return null;

            ItemStack selectedBow = inv.getItem(bowSlot);
            if (selectedBow.isEmpty() || !(selectedBow.getItem() instanceof BowItem)) return null;
            if (!ItemStack.isSameItemSameComponents(selectedBow, weaponStack)) return null;

            // The row directly above the hotbar in the inventory grid is bowSlot + 9
            int aboveSlot = bowSlot + 9;
            ItemStack above = inv.getItem(aboveSlot);
            if (above.isEmpty() || !(above.getItem() instanceof ArrowItem)) return null;

            return above;
        } catch (Exception e) {
            return null;
        }
    }
}
