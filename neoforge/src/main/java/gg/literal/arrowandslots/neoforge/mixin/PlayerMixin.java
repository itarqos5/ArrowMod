package gg.literal.arrowandslots.neoforge.mixin;

import gg.literal.arrowandslots.ArrowSlotHelper;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(Player.class)
public abstract class PlayerMixin {

    @Inject(method = "getProjectile", at = @At("RETURN"), cancellable = true)
    private void arrowandslots$getArrowFromSlotAbove(ItemStack weaponStack, CallbackInfoReturnable<ItemStack> cir) {
        Player self = (Player) (Object) this;
        ItemStack arrow = ArrowSlotHelper.findArrowAbove(self);
        if (arrow != null) {
            cir.setReturnValue(arrow);
        }
    }
}