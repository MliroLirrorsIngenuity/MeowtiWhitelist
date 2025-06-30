<div align="center">
  <h1 align="center">MeowtiWhitelist</h1>
  <p align="center">
    一款基于 <a href="https://mcdreforged.com/"><strong>MCDReforged</strong></a> 开发的多验证服务白名单管理插件，解决多验证服务环境下的白名单问题。
    <br />
    <br />
    <a href="https://github.com/MliroLirrorsIngenuity/MeowtiWhitelist/blob/main/README.md">简体中文</a>
    |
    <a href="https://github.com/MliroLirrorsIngenuity/MeowtiWhitelist/blob/main/README_EN.md">English</a>
  </p>
</div>

<details>
  <summary>目录</summary>

  - [特性](#特性)
  - [使用方式](#使用方式)
    - [依赖](#依赖)
    - [安装](#安装)
    - [配置&指令&API](#配置指令api)
  - [提问前必看](#提问前必看)
  - [贡献者](#贡献者)
  - [致谢](#致谢)

</details>

## 特性

  - 解决使用多个不同 **Yggdrasil** 验证服务导致的UUID冲突或不正确的问题。
  - 使用简单命令，管理来自不同 **Yggdrasil** 验证来源的白名单添加。
  - 不再需要手动添加对应验证来源的正确UUID到 `whitelist.json` 。 ~~不是哥们谁又手动改`whitelist.json`~~
  - 我们提供了一系列API供开发者调用，你可以使用本插件来管理并获取多个来源的UUID。

## 使用方式

### 依赖

`MCDReforged`>=2.12.0

`requests`>=2.31.0

`PyYAML`>=6.0.2

### 安装

在运行的 MCDReforged 实例中执行以下命令，根据提示引导进行安装。
```
!!MCDR plugin install meowtiwhitelist
```

如果服务端网络环境访问安装源存在困难，可以尝试下面的手动安装

<details>
  <summary>手动安装</summary>

1. 从 [GitHub Releases](https://github.com/MliroLirrorsIngenuity/MeowtiWhitelist/releases)中下载最新版本的 MeowtiWhitelist
2. 将下载的插件放入MCDR的`plugins`目录中
3. 安装所需的[依赖](#依赖)
4. [通过MCDReforged启动服务器](https://docs.mcdreforged.com/zh-cn/latest/quick_start/first_run.html#run)

</details>

## 配置&指令&API
详见 [Wiki](https://github.com/MliroLirrorsIngenuity/MeowtiWhitelist/wiki)

## 提问前必看

> "运营团队，或是帮助你的人，并不是神 "
> <div align="right"> —— 《LittleSkin 用户使用手册》 </div>

在提问之前，请确保：

- 已经尝试了所有可能的解决方案

- 已经尝试搜索了解决方案（包括但不限于本仓库的[Issues](https://github.com/MliroLirrorsIngenuity/MeowtiWhitelist/issues)）

- 你提供了**足够的信息**帮助开发人员定位问题，包括但不限于下列：

  - 服务端日志（MCDR日志、服务端日志等）

  - 插件配置文件

  - 插件列表

  - MCDR 版本号、Minecraft 服务端版本号和插件版本号

## 贡献者
<a href="https://github.com/MliroLirrorsIngenuity/MeowtiWhitelist/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=MliroLirrorsIngenuity/MeowtiWhitelist&" alt="Contributors" />
</a>

## 致谢

[Lazy-Bing-Server/MCDR-offline-whitelist-manager](https://github.com/Lazy-Bing-Server/MCDR-offline-whitelist-manager)：提供了插件主体构建思路

[CaaMoe/MultiLogin](https://github.com/CaaMoe/MultiLogin)：提供了配置插件的方案灵感

[LittleSkinChina/manual-ng](https://github.com/LittleSkinChina/manual-ng)：提供了提问前必看的内容灵感 (CC-BY-SA 4.0)
