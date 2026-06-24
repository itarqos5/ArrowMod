package gg.literal.arrowandslots;

import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArrowItem;
import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;

public final class ArrowSlotHelper {
    private ArrowSlotHelper() {}

    /**
     * Returns the arrow ItemStack from the inventory slot directly above the bow
     * (bowSlot + 9), or null if no usable arrow is found there.
     *
     * Slot identification strategy:
     *  1. Object-identity check  – fast; works when weaponStack IS the inventory slot reference.
     *  2. isSameItemSameComponents – handles the case where Minecraft stores a copy
     *     of the use-item (e.g. in LivingEntity.useItem on some versions).
     */
    @Nullable
    public static ItemStack findArrowAbove(Player player, ItemStack weaponStack) {
        try {
            if (weaponStack.isEmpty() || !(weaponStack.getItem() instanceof BowItem)) return null;

            Inventory inv = player.getInventory();
            int bowSlot = -1;

            // Pass 1 – identity (same object reference)
            for (int i = 0; i < 9; i++) {
                if (inv.getItem(i) == weaponStack) {
                    bowSlot = i;
                    break;
                }
            }

            // Pass 2 – full component match (handles copied stacks)
            if (bowSlot == -1) {
                for (int i = 0; i < 9; i++) {
                    ItemStack s = inv.getItem(i);
                    if (!s.isEmpty()
                            && s.getItem() instanceof BowItem
                            && ItemStack.isSameItemSameComponents(s, weaponStack)) {
                        bowSlot = i;
                        break;
                    }
                }
            }

            if (bowSlot == -1) return null;

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
