package org.MliroLirrorsIngenuity.meowtiWhitelist.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class whitelistConfig {
    private final Path configDir;
    private final Path configFile;
    private final Gson gson;

    // Map of Yggdrasil servers to whitelisted players
    private Map<String, Set<String>> whitelistedPlayers = new ConcurrentHashMap<>();

    // Default Mojang Yggdrasil servers
    private static final String MOJANG_YGGDRASIL = "https://sessionserver.mojang.com";

    // Default LittleSkin Yggdrasil server
    private static final String LITTLESKIN_YGGDRASIL = "https://littleskin.cn/sessionserver"; // IDK is this is real, even the writer (@FLYEMOJ1) are LittleSkinCommspt, someone please confirm this.
    public whitelistConfig(Path dataDirectory) {
        this.configDir = dataDirectory;
        this.configFile = configDir.resolve("whitelist.json");
        this.gson = new GsonBuilder().setPrettyPrinting().create();

        // Initialize with default Mojang Yggdrasil
        whitelistedPlayers.put(MOJANG_YGGDRASIL, new HashSet<>());
    }

    public void load() {
        try {
            if (!Files.exists(configDir)) {
                Files.createDirectories(configDir);
            }

            if (Files.exists(configFile)) {
                try (Reader reader = Files.newBufferedReader(configFile)) {
                    whitelistedPlayers = gson.fromJson(reader,
                            new TypeToken<Map<String, Set<String>>>(){}.getType());
                }
            } else {
                save(); // Create default config
            }
        } catch (IOException e) {
            e.printStackTrace(); // TODO: Change This to Throwable.
        }
    }

    public void save() {
        try {
            if (!Files.exists(configDir)) {
                Files.createDirectories(configDir);
            }

            try (Writer writer = Files.newBufferedWriter(configFile)) {
                gson.toJson(whitelistedPlayers, writer);
            }
        } catch (IOException e) {
            e.printStackTrace(); // TODO: Change This to Throwable.
        }
    }

    public boolean isWhitelisted(String yggdrasilServer, String username) {
        Set<String> players = whitelistedPlayers.get(yggdrasilServer);
        return players != null && players.contains(username.toLowerCase());
    }

    public void addToWhitelist(String yggdrasilServer, String username) {
        whitelistedPlayers.computeIfAbsent(yggdrasilServer, k -> new HashSet<>())
                .add(username.toLowerCase());
        save();
    }

    public void removeFromWhitelist(String yggdrasilServer, String username) {
        Set<String> players = whitelistedPlayers.get(yggdrasilServer);
        if (players != null) {
            players.remove(username.toLowerCase());
            save();
        }
    }

    public Set<String> getYggdrasilServers() {
        return new HashSet<>(whitelistedPlayers.keySet());
    }

    public Set<String> getWhitelistedPlayers(String yggdrasilServer) {
        return whitelistedPlayers.getOrDefault(yggdrasilServer, Collections.emptySet());
    }
}