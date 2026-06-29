package gg.literal.arrowandslots.fabric.mixin;

import gg.literal.arrowandslots.ArrowSlotHelper;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(Player.class)
public abstract class PlayerMixin {

    /**
     * Intercepts the arrow-selection return value of Player#getProjectile.
     * If the slot directly above the held bow contains an arrow of any type
     * (normal, tipped, spectral), that arrow is returned instead, causing
     * the bow to consume and fire it.
     *
     * require = 1 so a failed injection is caught at startup, not silently swallowed.
     */
    @Inject(method = "getProjectile", at = @At("RETURN"), cancellable = true, require = 1)
    private void arrowandslots$getArrowFromSlotAbove(
            ItemStack weaponStack, CallbackInfoReturnable<ItemStack> cir) {
        try {
            Player self = (Player) (Object) this;
            ItemStack arrow = ArrowSlotHelper.findArrowAbove(self, weaponStack);
            if (arrow != null) {
                cir.setReturnValue(arrow);
            }
        } catch (Exception ignored) {
        }
    }
}
