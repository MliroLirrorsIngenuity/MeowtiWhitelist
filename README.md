# MultiWhitelist

MultiWhitelist 是一款基于 [MCDReforged](https://mcdreforged.com/) 开发的多验证服务白名单管理插件。

使用本插件，可以：

- 解决使用多个不同 Yggdrasil 验证服务导致的UUID冲突或不同的问题。
- 简单一行，管理来自不同 **Yggdrasil** 验证来源的白名单添加。
- ~~不是哥们谁又手动改`whitelist.json`~~

## 提问前必看

> "运营团队，或是帮助你的人，并不是神 "
> <div style="text-align: right">—— 《LittleSkin 用户使用手册》</div>

在提问之前，请确保：

- 已经尝试了所有可能的解决方案

- 已经尝试搜索了解决方案（包括但不限于本仓库的[Issues](https://github.com/MliroLirrorsIngenuity/MultiWhitelist/issues)）

- 你提供了**足够的信息**帮助开发人员定位问题，包括但不限于下列：

  - 服务端日志（MCDR日志、服务端日志等）

  - 插件配置文件

  - 插件列表

  - MCDR版本号、MC服务端版本号和插件版本号

## 目录

- [提问前必看](#提问前必看)
- [使用方式](#使用方式)
  - [安装](#安装)
  - [配置](#配置)
    - [找到配置文件](#找到配置文件)
    - [启用验证服务](#启用验证服务)

## 使用方式

### 安装

~~把大象装进冰箱需要几步~~

- 从 [GitHub Releases](https://github.com/MliroLirrorsIngenuity/MultiWhitelist/releases)中下载最新版本的MultiWhitelist
- 将下载的插件放入`plugins`目录中（如下所示）

```bash
    your_mcdr_server/
    ├─ config/
    ├─ logs/
    ├─ plugins/
        ├─ ...
++  │   └─ MultiWhitelist-v{x.y.z}.mcdr
    ├─ server/
    ├─ config.yml
    └─ permission.yml
```

- [通过MCDReforged启动服务器](https://docs.mcdreforged.com/zh-cn/latest/quick_start/first_run.html#run)

### 配置

#### 找到配置文件

在安装插件以后，你还需要为插件配置服务。为了方便使用，我们已经提前内置好了主要验证方式的模板。

在首次运行之后，插件将会释放配置文件，并存放在`config`目录之中，如下所示。

```bash
    your_mcdr_server/config
    ├── mcdreforged
    │   └── ...
++  └── MultiWhitelist
        ├── config.json
        ├── example
        │   ├── littleskin.yml
        │   └── mojang.yml
        └── service
```

- `littleskin.yml` 是 LittleSkin 验证服务的模板
- `mojang.yml` 是 Mojang 官方正版验证服务的模板

#### 启用验证服务

此处使用 **LittleSkin** 的配置文件模板 `littleskin.yml` 为例。

``` yaml littleskin.yml

# Please edit before use.
id: 0

name: 'LittleSkin'
# Don't change it unless you really want to.
serviceType: BLESSING_SKIN
yggdrasilAuth:
  blessingSkin:
    apiRoot: 'https://littleskin.cn/api/yggdrasil'

```

- `id` 是验证服务使用的序号，从1开始。

当您将配置文件修改完毕后，请将 `littleskin.yml` **移动**或**复制**为以下状态。

``` bash

    your_mcdr_server/config
    ├── mcdreforged
    │   └── ...
++  └── MultiWhitelist
        ├── config.json
        ├── example
        │   ├── littleskin.yml
          └── mojang.yml
        └── service
        │   ├── littleskin.yml

```
