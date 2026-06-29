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
    public static ItemStack findArrowAbove(Player player, ItemStack weaponStack) {
        try {
            if (weaponStack.isEmpty() || !(weaponStack.getItem() instanceof BowItem)) return null;

            Inventory inv = player.getInventory();

            // Scan hotbar slots 0-8 to find which slot holds this bow.
            // Avoids any direct access to the private `selected` field.
            int bowSlot = -1;
            for (int i = 0; i < 9; i++) {
                ItemStack slot = inv.getItem(i);
                if (!slot.isEmpty()
                        && slot.getItem() instanceof BowItem
                        && ItemStack.isSameItemSameComponents(slot, weaponStack)) {
                    bowSlot = i;
                    break;
                }
            }
            if (bowSlot < 0) return null;

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
