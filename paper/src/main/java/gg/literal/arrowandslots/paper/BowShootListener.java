package gg.literal.arrowandslots.paper;

import org.bukkit.GameMode;
import org.bukkit.Material;
import org.bukkit.entity.Arrow;
import org.bukkit.entity.Player;
import org.bukkit.entity.SpectralArrow;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityShootBowEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.PlayerInventory;
import org.bukkit.inventory.meta.PotionMeta;
import org.bukkit.util.Vector;

import java.util.Set;

public final class BowShootListener implements Listener {

    private static final Set<Material> ARROW_MATERIALS = Set.of(
        Material.ARROW,
        Material.TIPPED_ARROW,
        Material.SPECTRAL_ARROW
    );

    @EventHandler
    public void onShoot(EntityShootBowEvent event) {
        if (!(event.getEntity() instanceof Player player)) return;

        PlayerInventory inv = player.getInventory();
        int selected = inv.getHeldItemSlot();
        int aboveSlot = selected + 9;
        if (aboveSlot >= inv.getSize()) return;

        ItemStack aboveStack = inv.getItem(aboveSlot);
        if (aboveStack == null || !ARROW_MATERIALS.contains(aboveStack.getType())) return;

        boolean creative = player.getGameMode() == GameMode.CREATIVE;

        Vector velocity = event.getProjectile().getVelocity();

        event.setCancelled(true);

        if (aboveStack.getType() == Material.SPECTRAL_ARROW) {
            player.launchProjectile(SpectralArrow.class, velocity);
        } else {
            Arrow arrow = player.launchProjectile(Arrow.class, velocity);
            if (aboveStack.getType() == Material.TIPPED_ARROW
                && aboveStack.getItemMeta() instanceof PotionMeta meta) {
                arrow.setBasePotionData(meta.getBasePotionData());
            }
        }

        if (!creative) {
            aboveStack.setAmount(aboveStack.getAmount() - 1);
            if (aboveStack.getAmount() <= 0) {
                inv.setItem(aboveSlot, null);
            } else {
                inv.setItem(aboveSlot, aboveStack);
            }
        }
    }
}