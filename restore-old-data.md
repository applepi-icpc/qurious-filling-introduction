## 恢复旧版游猫网配装器中储存的数据

游猫网全站近日完成了从 HTTP 到 HTTPS 的升级。然而，这一升级将会导致您的浏览器中储存的数据不能访问（因为 https://gamecat.fun 和 http://gamecat.fun 是不同的 HOST，由于同源策略的限制，浏览器将阻止程序访问旧数据）。

为了让您能读取并恢复您的旧数据，我们开发了一个小工具。如果您有需要，请按照下列步骤操作。

对此带来的不便，我们深感歉意！有任何问题，请联系 gamecat@aliyun.com 询问。

### 目录

- [恢复旧版游猫网配装器中储存的数据](#恢复旧版游猫网配装器中储存的数据)
  - [目录](#目录)
  - [Windows 系统](#windows-系统)
  - [macos 系统](#macos-系统)
  - [常见问题：Chrome 浏览器](#常见问题chrome-浏览器)

### Windows 系统

首先，如果您使用了任何代理软件 (例如梯子)，请将它们关闭。

点击开始菜单，然后点击齿轮图标进入系统设置；

![](https://gamecat.fun/s/win1.jpg)

在设置中，点击“网络和 Internet”；

![](https://gamecat.fun/s/win2.jpg)

在左侧点击“代理”；在右侧打开“使用代理服务器”选项，在地址中填写 `p.gamecat.fun`，在端口中填写 `9000`，然后点击保存；

![](https://gamecat.fun/s/win3.jpg)

打开您之前使用游猫网配装器的浏览器，在地址栏中输入 `http://gamecat.fun/httpisstupid`；

**注意**，前缀的 `http://` 不能省略，更不能写成 `https://`；

![](https://gamecat.fun/s/win4.jpg)

如果一切顺利，您将会打开我们的旧数据转移程序。浏览器会自动提示您下载压缩包；

如果您使用 Chrome 浏览器，由于 Chrome 浏览器奇怪的缓存和强制 HTTPS 机制，您可能会遇到问题。您可以在[这里](#常见问题chrome-浏览器)查看解决方法；

![](https://gamecat.fun/s/win5.jpg)

下载完成后，其中应当有 `favorite_sets.txt`，`talismans.txt` 和 `qurious_crafting.txt` 三个文件；

![](https://gamecat.fun/s/win6.jpg)

重新按照上述步骤回到代理设置，关闭“使用代理服务器”选项；

![](https://gamecat.fun/s/win7.jpg)

然后，您就可以打开游猫网配装器，在【配装收藏】，【护石列表】和【怪异炼化记录】中分别导入 `favorite_sets.txt` (**注意**，不是 `favorite_sets_raw.txt`)，`talismans.txt` 和 `qurious_crafting.txt` 三个文件了。

**注意**：导入将会覆盖您现有的记录。如果要合并两个记录，您需要点击“导入并合并”按钮。

### macos 系统

首先，如果您使用了任何代理软件 (例如梯子)，请将它们关闭。

进入“系统偏好设置”，然后点击“网络”；

![](https://gamecat.fun/s/mac1.jpg)

在左侧选择您正在使用的网络接口（一般为 Wi-Fi），然后点击右下角的“高级…”按钮；

![](https://gamecat.fun/s/mac2a.jpg)

进入“代理”选项卡，在左侧分别选择 “网页代理 (HTTP)” 和 “安全网页代理 (HTTPS)” 选项，在左侧将它们勾选，并在右侧设置代理服务器为 `p.gamecat.fun:9000`，然后点击“好”；

**注意**，两个选项右侧的代理设置都需要填；

![](https://gamecat.fun/s/mac3.jpg)

点击右下角的“应用”；

![](https://gamecat.fun/s/mac4.jpg)

打开您之前使用游猫网配装器的浏览器，在地址栏中输入 `http://gamecat.fun/httpisstupid`；

**注意**，前缀的 `http://` 不能省略，更不能写成 `https://`；

![](https://gamecat.fun/s/mac5.jpg)

如果一切顺利，您将会打开我们的旧数据转移程序。浏览器会自动提示您下载压缩包；

如果您使用 Chrome 浏览器，由于 Chrome 浏览器奇怪的缓存和强制 HTTPS 机制，您可能会遇到问题。您可以在[这里](#常见问题chrome-浏览器)查看解决方法；

![](https://gamecat.fun/s/mac6.jpg)

下载完成后，其中应当有 `favorite_sets.txt`，`talismans.txt` 和 `qurious_crafting.txt` 三个文件；

![](https://gamecat.fun/s/mac7.jpg)

重新按照上述步骤回到代理设置，取消勾选“网页代理 (HTTP)” 和 “安全网页代理 (HTTPS)”选项，点击“好”；

![](https://gamecat.fun/s/mac8.jpg)

然后点击右下角的“应用”，删除代理设置；

![](https://gamecat.fun/s/mac4.jpg)

然后，您就可以打开游猫网配装器，在【配装收藏】，【护石列表】和【怪异炼化记录】中分别导入 `favorite_sets.txt` (**注意**，不是 `favorite_sets_raw.txt`)，`talismans.txt` 和 `qurious_crafting.txt` 三个文件了。

**注意**：导入将会覆盖您现有的记录。如果要合并两个记录，您需要点击“导入并合并”按钮。

### 常见问题：Chrome 浏览器

由于 Chrome 浏览器奇怪的缓存和强制 HTTPS 机制，您可能会遇到问题，浏览器提示“gamecat.fun 未发送任何数据”；

![](https://gamecat.fun/s/chrome1.jpg)

首先，先在地址栏中输入 `chrome://settings/system`，进入 Chrome 的系统设置；

如果您看到“Chrome 使用的是由某款扩展程序指定的代理设置”，您需要首先停用或者删除这款扩展程序；

![](https://gamecat.fun/s/chrome7.jpg)

如果您看到“打开您计算机的代理设置”（或者，在停用/删除扩展程序后看到这行字），那么就没有问题，可以进行下一步了；

![](https://gamecat.fun/s/chrome8.jpg)

接下来，您可以点击地址栏右侧的三个点，打开菜单，选择“更多工具”子菜单，然后打开“开发者工具”；

![](https://gamecat.fun/s/chrome2.jpg)

在开发者工具中，进入“Network”选项卡，勾选“Disable cache”选项；

![](https://gamecat.fun/s/chrome3.jpg)

一些同学可能使用的是中文版的开发者工具，这时您可以进入“网络”选项卡，勾选“停用缓存”；

![](https://gamecat.fun/s/chrome4.jpg)

然后，**保持开发者工具打开，不要关闭**，在地址栏中，将光标移动到最左边，把 `https` 改为 `http`；

![](https://gamecat.fun/s/chrome5.jpg)

之后回车，您应该就可以进入旧数据转移程序了。如果仍有问题，可以尝试刷新一次；

![](https://gamecat.fun/s/chrome6.jpg)
