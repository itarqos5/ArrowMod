package gg.literal.arrowandslots.paper;

import org.bukkit.plugin.java.JavaPlugin;

public class ArrowAndSlotsPaper extends JavaPlugin {
    @Override
    public void onEnable() {
        getServer().getPluginManager().registerEvents(new BowShootListener(), this);
    }
}