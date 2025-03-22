package org.MliroLirrorsIngenuity.meowtiWhitelist.listener;

import com.velocitypowered.api.event.ResultedEvent;
import com.velocitypowered.api.event.Subscribe;
import com.velocitypowered.api.event.connection.LoginEvent;
import com.velocitypowered.api.event.connection.PreLoginEvent;
import com.velocitypowered.api.event.player.GameProfileRequestEvent;
import net.kyori.adventure.text.Component;
import org.MliroLirrorsIngenuity.meowtiWhitelist.MeowtiWhitelist;

public class ConnectionListener {
    private final MeowtiWhitelist plugin;

    public ConnectionListener(MeowtiWhitelist plugin) {
        this.plugin = plugin;
    }

    @Subscribe
    public void onGameProfileRequest(GameProfileRequestEvent event) {
        // This is where we can detect the Yggdrasil server
        // For now we'll use a simplified approach
        String username = event.getUsername();
        String yggdrasilServer = determineYggdrasilServer(event);

        if (!plugin.getWhitelistConfig().isWhitelisted(yggdrasilServer, username)) {
            event.setResult(GameProfileRequestEvent.Result.denied());
            plugin.getLogger().info("Player " + username + " denied access (not whitelisted for " + yggdrasilServer + ")");
        }
    }

    @Subscribe
    public void onLogin(LoginEvent event) {
        String username = event.getPlayer().getUsername();
        String yggdrasilServer = determineYggdrasilServer(event.getPlayer());

        if (!plugin.getWhitelistConfig().isWhitelisted(yggdrasilServer, username)) {
            event.setResult(ResultedEvent.ComponentResult.denied(
                    Component.text("You are not whitelisted on this server!")));
            plugin.getLogger().info("Player " + username + " denied access (not whitelisted for " + yggdrasilServer + ")");
        }
    }

    private String determineYggdrasilServer(GameProfileRequestEvent event) {
        // In a real implementation, you would extract the authentication server information
        // This is simplified, and you'll need to implement logic to determine the actual Yggdrasil server
        return "https://sessionserver.mojang.com";
    }

    private String determineYggdrasilServer(com.velocitypowered.api.proxy.Player player) {
        // In a real implementation, you would extract the authentication server information
        // from the player's connection metadata
        return "https://sessionserver.mojang.com";
    }
}