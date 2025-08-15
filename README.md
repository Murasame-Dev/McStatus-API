# McStatus-API
这是一个 Flask API，主要封装了 mcstatus 包，用于查询 Minecraft 服务器状态，支持Java和基岩，以及附带其他小特性！

## 💻用法

此项目的页面模板正在筹备中，敬请等待！

- `GET /java?ip=<IP> - (Required)` - 查询 Java 版服务器状态
- `GET - /bedrock?ip=<IP> - (Required)` - 查询基岩版服务器状态

## 📦安装&▶启动

以下提到的方法 任选**其一** 即可

<details open>
<summary>uv</summary>

```bash
uv run app.py
```
  
</details>

<details open>
<summary>pdm</summary>

```bash
pdm install
pdm run app.py
```
</details>

<details open>
<summary>pip</summary>

```bash
pip install -r requirements.txt
python app.py
```
</details>

## 🖊下一步计划
1. **添加配置文件**   
2. 添加一个基于此项目的服务端(他可能只是一个API Caller，或者是一个Websocket服务器？)   
服务端可以调用多个API，并将其返回的信息进行合并并输出，旨在用于检查不同地区的延迟
3. 添加是否默认使用 SRV 解析的变量
4. *等一切尘埃落定后，我会考虑使用 FastAPI*

## 📞 联系

TG群组：[点此加入](https://t.me/LoveMurasame)   
吹水群：[1049319982](https://qm.qq.com/q/DfTsIDXuc8)   
邮箱：<congyu@sbhfy.cn>   
