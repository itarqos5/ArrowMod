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

            ItemStack mainHand = player.getMainHandItem();
            if (mainHand.isEmpty() || !(mainHand.getItem() instanceof BowItem)) return null;
            if (!ItemStack.isSameItemSameComponents(mainHand, weaponStack)) return null;

            Inventory inv = player.getInventory();
            int bowSlot = -1;

            // The selected hotbar slot is the one whose stack is the player's current main-hand stack.
            for (int i = 0; i < 9; i++) {
                if (inv.getItem(i) == mainHand) {
                    bowSlot = i;
                    break;
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
