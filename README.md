# Luogu-Image 一个方便快捷的洛谷图床客户端

## 使用方法

### 配置文件

在编译后的程序同目录下编辑一个 `setting.json` 格式如下：

>  [!CAUTION]
>
> 如果不放置 `setting.json` 可能会有意想不到的结果。

```json
{
    "mode": 1,
    "//": "洛谷图床的储存模式，0 为无水印，1 为 Logo，2 为 Logo@Username"
    "_uid": 123456,
    "//": "你的 uid (_uid)"
    "__client_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    "//": "你的 cookie (__client_id)"
}
```

### 上传图片

运行编译后的程序，将 `.png` 图像直接拖入窗口即可，链接会自动复制到剪切板。

> [!NOTE]
>
> 目前仅支持 `.png` 图像。

> [!WARNING]
>
> 由于洛谷的限制，每日最多可上传 50 张图片，同时请注意高级空间的消耗。

## 自行构建

```shel
git clone https://github.com/CodingOIer/Luogu-Image
cd ./Luogu-Image
pip install ./requirements.txt
pyinstaller -icon logo.ico -F ./main.py
```