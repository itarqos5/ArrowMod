package gg.literal.arrowandslots.paper;

import org.bukkit.GameMode;
import org.bukkit.Material;
import org.bukkit.enchantments.Enchantment;
import org.bukkit.entity.AbstractArrow;
import org.bukkit.entity.Arrow;
import org.bukkit.entity.Player;
import org.bukkit.entity.SpectralArrow;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityShootBowEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.PlayerInventory;
import org.bukkit.inventory.meta.PotionMeta;
import org.bukkit.potion.PotionEffect;
import org.bukkit.util.Vector;

import java.util.Set;

public final class BowShootListener implements Listener {

    private static final Set<Material> ARROW_MATERIALS = Set.of(
        Material.ARROW,
        Material.TIPPED_ARROW,
        Material.SPECTRAL_ARROW
    );

    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onShoot(EntityShootBowEvent event) {
        try {
            if (!(event.getEntity() instanceof Player player)) return;
            if (!(event.getProjectile() instanceof AbstractArrow originalArrow)) return;

            PlayerInventory inv = player.getInventory();
            int selected = inv.getHeldItemSlot();
            int aboveSlot = selected + 9;
            if (aboveSlot < 0 || aboveSlot >= inv.getSize()) return;

            ItemStack aboveStack = inv.getItem(aboveSlot);
            if (aboveStack == null || !ARROW_MATERIALS.contains(aboveStack.getType())) return;

            boolean creative = player.getGameMode() == GameMode.CREATIVE;

            // Capture original arrow physics so they survive the entity swap
            Vector velocity   = originalArrow.getVelocity().clone();
            double  damage    = originalArrow.getDamage();
            int     knockback = originalArrow.getKnockbackStrength();
            boolean critical  = originalArrow.isCritical();
            AbstractArrow.PickupStatus pickup =
                    creative ? AbstractArrow.PickupStatus.CREATIVE_ONLY
                             : AbstractArrow.PickupStatus.ALLOWED;

            // Apply Power enchantment damage bonus (0.5 + level * 0.5 per half-heart)
            ItemStack bow = event.getBow();
            if (bow != null) {
                int power = bow.getEnchantmentLevel(Enchantment.POWER);
                if (power > 0) {
                    damage = damage + power * 0.5 + 0.5;
                }
                int punch = bow.getEnchantmentLevel(Enchantment.PUNCH);
                if (punch > 0) {
                    knockback = Math.max(knockback, punch);
                }
            }

            event.setCancelled(true);

            AbstractArrow newArrow;
            if (aboveStack.getType() == Material.SPECTRAL_ARROW) {
                newArrow = player.launchProjectile(SpectralArrow.class, velocity);
            } else {
                Arrow arrow = player.launchProjectile(Arrow.class, velocity);
                if (aboveStack.getType() == Material.TIPPED_ARROW) {
                    applyPotionData(aboveStack, arrow);
                }
                newArrow = arrow;
            }

            newArrow.setDamage(damage);
            newArrow.setKnockbackStrength(knockback);
            newArrow.setCritical(critical);
            newArrow.setPickupStatus(pickup);

            if (!creative) {
                aboveStack.setAmount(aboveStack.getAmount() - 1);
                inv.setItem(aboveSlot, aboveStack.getAmount() > 0 ? aboveStack : null);
            }
        } catch (Exception ignored) {
        }
    }

    /**
     * Copies potion data from a TIPPED_ARROW ItemStack onto a fired Arrow entity.
     * Uses the non-deprecated API available in Paper 1.20.6+.
     */
    private void applyPotionData(ItemStack source, Arrow target) {
        try {
            if (!(source.getItemMeta() instanceof PotionMeta meta)) return;

            // Base potion type (replaces deprecated setBasePotionData)
            if (meta.getBasePotionType() != null) {
                target.setBasePotionType(meta.getBasePotionType());
            }

            // Custom effects stacked on top
            for (PotionEffect effect : meta.getCustomEffects()) {
                target.addCustomEffect(effect, true);
            }

            // Tint colour (may be null on uncoloured arrows)
            if (meta.hasColor()) {
                target.setColor(meta.getColor());
            }
        } catch (Exception ignored) {
        }
    }
}
