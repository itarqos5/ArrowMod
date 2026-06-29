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
        return findArrowAbove(player, -1, weaponStack);
    }

    @Nullable
    public static ItemStack findArrowAbove(Player player, int bowSlot, ItemStack weaponStack) {
        try {
            if (weaponStack.isEmpty() || !(weaponStack.getItem() instanceof BowItem)) return null;

            Inventory inv = player.getInventory();

            // If a valid hotbar slot wasn't provided or doesn't hold the weapon, scan hotbar slots 0-8
            if (bowSlot < 0 || bowSlot >= 9 || !ItemStack.isSameItemSameComponents(inv.getItem(bowSlot), weaponStack)) {
                bowSlot = -1;
                for (int i = 0; i < 9; i++) {
                    ItemStack slot = inv.getItem(i);
                    if (!slot.isEmpty()
                            && slot.getItem() instanceof BowItem
                            && ItemStack.isSameItemSameComponents(slot, weaponStack)) {
                        bowSlot = i;
                        break;
                    }
                }
            }
            if (bowSlot < 0) return null;

            // In Minecraft PlayerInventory:
            // Slots 0-8: Hotbar (bottom row on screen)
            // Slots 27-35: Bottom row of main inventory (directly above hotbar on screen)
            // Slots 18-26: Middle row of main inventory
            // Slots 9-17: Top row of main inventory
            int directlyAbove = bowSlot + 27;
            ItemStack above = inv.getItem(directlyAbove);
            if (!above.isEmpty() && above.getItem() instanceof ArrowItem) {
                return above;
            }

            // Fallback check 2 rows above (18 + bowSlot) and 3 rows above (9 + bowSlot)
            int twoAbove = bowSlot + 18;
            above = inv.getItem(twoAbove);
            if (!above.isEmpty() && above.getItem() instanceof ArrowItem) {
                return above;
            }

            int threeAbove = bowSlot + 9;
            above = inv.getItem(threeAbove);
            if (!above.isEmpty() && above.getItem() instanceof ArrowItem) {
                return above;
            }

            return null;
        } catch (Exception e) {
            return null;
        }
    }
}
