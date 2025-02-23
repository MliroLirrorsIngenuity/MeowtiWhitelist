# MultiWhitelist

MultiWhitelist 是一款基于 [MCDReforged](https://mcdreforged.com/) 开发的多验证服务白名单管理插件。

使用本插件，可以：

- 解决使用多个不同 Yggdrasil 验证服务导致的UUID冲突或不同的问题。
- ~~无需再费力确认`whitelist.json`到底改没改对~~
- 无需再费力确认白名单是否生效

## 目录

- [使用方式](#使用方式)
  - [安装](#安装)
  - [配置](#配置)
    - [找到配置文件](#找到配置文件)
    - [启用验证服务](#启用验证服务)
- [提问前必看](#提问前必看)

## 使用方式

### 安装

~~把大象装进冰箱需要几步~~

- 从 [GitHub Releases]中下载最新版本的MultiWhitelist
- 将下载的插件放入`plugins`目录中（如下所示）

```bash
    my_mcdr_server/
    ├─ config/
    ├─ logs/
    │   └─ MCDR.log
    ├─ plugins/
        ├─ ...
++  │   └─ MultiWhitelist-v{x.y.z}.mcdr
    ├─ server/
        ├─ ...
        ├─ minecraft_server.jar
        └─ server.properties
    ├─ config.yml
    └─ permission.yml
```

- [通过MCDReforged启动服务器](https://docs.mcdreforged.com/zh-cn/latest/quick_start/first_run.html#run)

### 配置

#### 找到配置文件

在安装插件以后，你还需要为插件配置服务。为了方便使用，我们已经提前内置好了模板。

在首次运行之后，插件将会释放配置文件，并存放在`config`目录之中，如下所示。

```bash
    my_mcdr_server/config
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

这里以 LittleSkin 的验证服务举例

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

## 提问前必看

WIP
