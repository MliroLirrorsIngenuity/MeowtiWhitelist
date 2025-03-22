package org.MliroLirrorsIngenuity.meowtiWhitelist;

import com.google.inject.Inject;
import com.velocitypowered.api.command.CommandManager;
import com.velocitypowered.api.event.proxy.ProxyInitializeEvent;
import com.velocitypowered.api.event.Subscribe;
import com.velocitypowered.api.plugin.Plugin;
import com.velocitypowered.api.plugin.annotation.DataDirectory;
import com.velocitypowered.api.proxy.ProxyServer;
import org.MliroLirrorsIngenuity.meowtiWhitelist.commands.WhitelistCommand;
import org.MliroLirrorsIngenuity.meowtiWhitelist.config.WhitelistConfig;
import org.MliroLirrorsIngenuity.meowtiWhitelist.listeners.ConnectionListener;
import org.slf4j.Logger;

import java.nio.file.Path;

@Plugin(id = "meowtiwhitelist", name = "MeowtiWhitelist", version = BuildConstants.VERSION, description = "A Whitelist Plugin for Multi Yggdrasil User/Servers.", url = "https://github.com/MliroLirrorsIngenuity", authors = {"MliroLirrorsIngenuity"})
public class MeowtiWhitelist {

    private final ProxyServer server;
    private final Logger logger;
    private final Path dataDirectory;
    private WhitelistConfig whitelistConfig;

    @Inject
    public MeowtiWhitelist(ProxyServer server, Logger logger, @DataDirectory Path dataDirectory) {
        this.server = server;
        this.logger = logger;
        this.dataDirectory = dataDirectory;
        this.whitelistConfig = new WhitelistConfig(dataDirectory);
    }

    @Subscribe
    public void onProxyInitialize(ProxyInitializeEvent event) {
        onEnable();
    }

    public void onEnable() {
        logger.info("Hi, MeowtiWhitelist Enabled!");

        // Load configuration
        whitelistConfig.load();

        // Register event listener
        server.getEventManager().register(this, new ConnectionListener(this));

        // Register commands
        CommandManager commandManager = server.getCommandManager();
        commandManager.register("meowtiwhitelist", new WhitelistCommand(this), "mwl");
    }

    public void onDisable() {
        logger.info("Bye, MeowtiWhitelist Disabled!");
        whitelistConfig.save();
    }

    public void onReload() {
        logger.info("Wow, MeowtiWhitelist Reloaded!");
        whitelistConfig.load();
    }

    public Logger getLogger() {
        return logger;
    }

    public ProxyServer getServer() {
        return server;
    }

    public WhitelistConfig getWhitelistConfig() {
        return whitelistConfig;
    }

    public Path getDataDirectory() {
        return dataDirectory;
    }
}