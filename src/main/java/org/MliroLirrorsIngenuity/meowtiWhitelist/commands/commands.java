package org.MliroLirrorsIngenuity.meowtiWhitelist.commands;

import com.velocitypowered.api.command.CommandSource;
import com.velocitypowered.api.command.SimpleCommand;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.MliroLirrorsIngenuity.meowtiWhitelist.MeowtiWhitelist;

import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

public class WhitelistCommand implements SimpleCommand {
    private final MeowtiWhitelist plugin;

    public WhitelistCommand(MeowtiWhitelist plugin) {
        this.plugin = plugin;
    }

    @Override
    public void execute(Invocation invocation) {
        CommandSource source = invocation.source();
        String[] args = invocation.arguments();

        if (args.length == 0) {
            showHelp(source);
            return;
        }

        switch (args[0].toLowerCase()) {
            case "add":
                if (args.length < 3) {
                    source.sendMessage(Component.text("Usage: /meowwhitelist add <yggdrasil-server> <player>", NamedTextColor.RED));
                    return;
                }
                plugin.getWhitelistConfig().addToWhitelist(args[1], args[2]);
                source.sendMessage(Component.text("Added " + args[2] + " to whitelist for " + args[1], NamedTextColor.GREEN));
                break;

            case "remove":
                if (args.length < 3) {
                    source.sendMessage(Component.text("Usage: /meowwhitelist remove <yggdrasil-server> <player>", NamedTextColor.RED));
                    return;
                }
                plugin.getWhitelistConfig().removeFromWhitelist(args[1], args[2]);
                source.sendMessage(Component.text("Removed " + args[2] + " from whitelist for " + args[1], NamedTextColor.GREEN));
                break;

            case "list":
                if (args.length < 2) {
                    source.sendMessage(Component.text("Usage: /meowwhitelist list <yggdrasil-server>", NamedTextColor.RED));
                    return;
                }
                Set<String> players = plugin.getWhitelistConfig().getWhitelistedPlayers(args[1]);
                source.sendMessage(Component.text("Whitelisted players for " + args[1] + ":", NamedTextColor.YELLOW));
                for (String player : players) {
                    source.sendMessage(Component.text("- " + player, NamedTextColor.WHITE));
                }
                break;

            case "servers":
                Set<String> servers = plugin.getWhitelistConfig().getYggdrasilServers();
                source.sendMessage(Component.text("Available Yggdrasil servers:", NamedTextColor.YELLOW));
                for (String server : servers) {
                    source.sendMessage(Component.text("- " + server, NamedTextColor.WHITE));
                }
                break;

            case "reload":
                plugin.getWhitelistConfig().load();
                source.sendMessage(Component.text("Whitelist reloaded!", NamedTextColor.GREEN));
                plugin.onReload();
                break;

            default:
                showHelp(source);
                break;
        }
    }

    private void showHelp(CommandSource source) {
        source.sendMessage(Component.text("MeowtiWhitelist Commands:", NamedTextColor.GOLD));
        source.sendMessage(Component.text("/meowwhitelist add <yggdrasil-server> <player> - Add a player to the whitelist", NamedTextColor.YELLOW));
        source.sendMessage(Component.text("/meowwhitelist remove <yggdrasil-server> <player> - Remove a player from the whitelist", NamedTextColor.YELLOW));
        source.sendMessage(Component.text("/meowwhitelist list <yggdrasil-server> - List all whitelisted players for a server", NamedTextColor.YELLOW));
        source.sendMessage(Component.text("/meowwhitelist servers - List all configured Yggdrasil servers", NamedTextColor.YELLOW));
        source.sendMessage(Component.text("/meowwhitelist reload - Reload the whitelist configuration", NamedTextColor.YELLOW));
    }

    @Override
    public List<String> suggest(Invocation invocation) {
        String[] args = invocation.arguments();

        if (args.length == 1) {
            return Arrays.asList("add", "remove", "list", "servers", "reload");
        } else if (args.length == 2) {
            if (args[0].equalsIgnoreCase("add") ||
                    args[0].equalsIgnoreCase("remove") ||
                    args[0].equalsIgnoreCase("list")) {
                return new ArrayList<>(plugin.getWhitelistConfig().getYggdrasilServers());
            }
        } else if (args.length == 3) {
            if (args[0].equalsIgnoreCase("remove")) {
                return new ArrayList<>(plugin.getWhitelistConfig().getWhitelistedPlayers(args[1]));
            }
        }

        return List.of();
    }
}