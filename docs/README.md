不久前刷到一个Steam游戏数据导入到notion的[帖子](https://api.xiaoheihe.cn/v3/bbs/app/api/web/share?link_id=92db70876995)，下面有人问能否在Obsidian中实现，虽然一开始不怎么想自己动手写一个，但因为放假了时间够，就用碎片时间摸出来了

原理还是调用Steam的api获取玩家的游戏列表，再逐个获取每个游戏的具体信息，然后写到目标文件夹，最后在Obsidian中通过[Projects](https://github.com/marcusolsson/obsidian-projects)插件展示出来
#### 准备.env文件
在程序所在目录创建一个`.env`文件，填写接下来我们获得的信息
##### 获取Steam api key
这里可以参考其他更详细的文章：[steamapikey怎么获取](https://www.bilibili.com/opus/864170441009266752)
获得api key后在`.env`文件中填写在`API_KEY=`后面，如`API_KEY=abcdefg123456789`
#### 找到自己的SteamID64
###### 最快速的方法是从Steam中直接获取
![s2o/docs/id.png at main · Yoak3n/s2o](https://github.com/Yoak3n/s2o/blob/main/docs/id.png?raw=true)
###### 通过第三方网站查询用户获取
随手找到一个网站，可以通过好友代码等来查询 https://id.ovohi.com/
![s2o/docs/lookup.png at main · Yoak3n/s2o](https://github.com/Yoak3n/s2o/blob/main/docs/lookup.png?raw=true)
同样可以得到这个`SteamID64`
获得这串ID后在`.env`文件中填写在`ID=`后面，如`ID=76561198401863143`
##### 填写要存放游戏数据的文件夹路径
由于Obsidian管理内容的最小单元是文件，因此需要每个游戏的数据单独创建一个文件来保存并存放在同一文件夹中，比如现在我们要存放在Obsidian库中来管理，以我自己的Obsidian库为例，将路径`E:\GitVault\daily\Resource\Game`直接复制下来
在`.env`文件中填写在`DIR=`后面，如`DIR=E:\GitVault\daily\Resource\Game`
	支持不存在该路径时创建该目录
#### 运行程序
准备好`.env`文件后就可以运行程序了，在获取完游戏列表后会有如下选项
```
========================================
1. 仅游玩时间超过 200 小时的游戏（6个）
2. 仅游玩时间超过 500 小时的游戏（5个）
3. 仅最近2个月游玩的游戏（15个）
4. 仅游玩过的游戏（70个）
5. 所有游戏（84个）
========================================
请选择导入游戏的范围（default=1）：
```
选择导入游戏的范围后，就会开始逐个获取游戏的更详细信息
获取信息完毕后，因为Steam游戏库中有一些非游戏的软件，可以选择是否过滤
```
是否忽略工具或软件？(y/N)
```
默认不忽略，输入`y`表示忽略
之后就会发现程序运行完成，所有游戏数据全部写到了我们在`.env`中指定的文件目录下，由于部分游戏名中有系统不允许在文件名中存在的非法字符，所以做了一些简单的替换
#### 在Obsidian中展示出来
##### 使用Projects插件
似乎因为这个插件仓库已归档不再更新，导致在Obsidian的社区插件仓库中无法直接搜索到
幸好Obdisian支持用`BRAT`插件安装一些官方仓库中的非正式插件，即插件选项中的`Add beta plugin`
![s2o/docs/plugin.png at main · Yoak3n/s2o](https://github.com/Yoak3n/s2o/blob/main/docs/plugin.png?raw=true)

填写`Projects`插件的github仓库地址：`https://github.com/marcusolsson/obsidian-projects`，并选择最新的`1.17.4`版本

安装好之后使用`Projects`在左边栏新增的按钮添加项目
![s2o/docs/project.png at main · Yoak3n/s2o](https://github.com/Yoak3n/s2o/blob/main/docs/project.png?raw=true)

填写好项目名和引用的数据所在路径即可显示出来

再经过一些简单的设置：
1. 创建`画册`视图
2. 图片源指定为`Cover`，填充方式`填充`
3. 开启自己想要展示出来的`字段`

排序后效果大致如下（会根据Obsidian使用的主题有一定配色差异）：
![s2o/docs/show.png at main · Yoak3n/s2o](https://github.com/Yoak3n/s2o/blob/main/docs/show.png?raw=true)

##### 使用Dataview插件
`Dataview`插件可以之间在社区插件仓库中直接下载安装，在代码块中指定语言为`dataview`即可根据查询到的文件数据渲染出视图
如:
```dataview
TABLE WITHOUT ID
"![](" + Cover + ")" as 封面,
PlayedHours as 时长,
Genres as 类型
FROM "Resource/Game"
```
注意一定要指定代码块的语言，再根据`Dataview`的[文档](https://blacksmithgu.github.io/obsidian-dataview/)写出需要的查询语句即可
	其中`FROM`后跟的是数据文件夹在当前Obsidian仓库中的相对路径

##### 官方支持数据库？
听说下个大版本Obsidian支持数据库，期待、观望