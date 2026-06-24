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
     * Returns the arrow in the hotbar slot directly above {@code bowSlot},
     * or null if that slot is empty / not an arrow / bow check fails.
     *
     * @param player   the shooting player
     * @param bowSlot  the hotbar index (0-8) of the bow being fired
     */
    @Nullable
    public static ItemStack findArrowAbove(Player player, int bowSlot) {
        try {
            if (bowSlot < 0 || bowSlot > 8) return null;

            Inventory inv = player.getInventory();

            // Verify the identified slot actually holds a bow right now
            ItemStack bowStack = inv.getItem(bowSlot);
            if (bowStack.isEmpty() || !(bowStack.getItem() instanceof BowItem)) return null;

            // The slot directly above in the inventory grid is bowSlot + 9
            int aboveSlot = bowSlot + 9;
            ItemStack above = inv.getItem(aboveSlot);
            if (above.isEmpty() || !(above.getItem() instanceof ArrowItem)) return null;

            return above;
        } catch (Exception e) {
            return null;
        }
    }
}
