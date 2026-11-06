# 安装与连接命令全表

本表是 [bootstrap-prompt.md](bootstrap-prompt.md) 的命令依据。全部来自当前仓库已发布文档，不发明命令、路径或包名。

## 来源

| 用途 | 来源 |
| --- | --- |
| 公开二进制镜像与 `install.sh` | `docs/operations/private-release-reference.md`；实时清单 `https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json` |
| 云端 skills 安装 | 主仓 `README.md`：`npx --yes skills add https://github.com/yeisme/yeisme-agent-my-skills --skill ... --yes` |
| AI 做剧 skills 云入口 | 主仓 `AGENTS.md`：`https://github.com/yeisme/ai-drama-skills` |
| Eikona setup | `cli/eikona/docs/commands/setup.md`（默认预览，`--yes` 才写；不 probe provider、不生成、不接受凭据；冲突返回 `eikona skills plan`） |
| Scaena setup / skills | `scaena setup auto`、`scaena skills install --runtimes auto --yes --agent`、`scaena skills doctor --agent`、`scaena doctor --agent` |
| Eikona remote | `cli/eikona/docs/commands/remote.md` |
| Scaena remote | `agent/scaena/docs/commands/remote.md` |
| 输出契约 | `docs/workflows/ai-native-cli-output-contract.md` |

## 占位符

| 占位符 | 含义 | 约束 |
| --- | --- | --- |
| `MODE` | `client` / `owner` | `owner` 仅用户明确选择时 |
| `EIKONA_ENDPOINT` / `SCAENA_ENDPOINT` | owner HTTP origin | 生产用 HTTPS；私网明文仅 IP literal + 显式端口 |
| `KEY_FILE_EIKONA` / `KEY_FILE_SCAENA` | 用户级 access key 文件绝对路径 | mode 0600；agent 只读路径，绝不读内容 |
| `PROJECT` | owner 侧 project id | 如 `project:drama-s01` / `drama-s01` |
| `STORY_PATH` | 剧本 / 小说文件绝对路径 | 由 Router 消费，bootstrap 不解析内容 |
| `RUNTIMES` | Agent runtime 列表 | `agents,codex`；`auto` 由 setup 自行判定 |

## 阶段 0 探测

```bash
command -v node; command -v npx; command -v python3; command -v curl
command -v eikona; command -v scaena; command -v scaena-api; command -v auctra
eikona --version 2>/dev/null; scaena --version 2>/dev/null
eikona setup --agent 2>/dev/null
scaena doctor --agent 2>/dev/null
curl -fsSL --max-time 10 https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json
```

`eikona setup --agent` 输出 `eikona.setup.v1` / `fact.*` / `action.next`；`scaena doctor --agent` 给 readiness。**先 `setup --agent` 预览，再审阅后 `--yes`**。

## 阶段 1 安装 CLI

```bash
python3 - <<'PY'
import json, urllib.request
c = json.load(urllib.request.urlopen("https://raw.githubusercontent.com/yeisme/yeisme-dist/main/catalog.json", timeout=10))
for p in c["products"]:
    print(p["name"], p["latest"].split("/")[-1])
PY
```

```bash
env -u GH_TOKEN -u GITHUB_TOKEN curl -fsSL https://raw.githubusercontent.com/yeisme/yeisme-dist/main/install.sh | bash -s -- <product> <version>
```

注意：

- 安装目录 `~/.yeisme/bin`，加入 PATH 后用 `--version` 核对。
- 版本必须来自 `catalog.json` 的 `latest`，不写死 tag。
- 匿名安装只用 `yeisme/yeisme-dist` 的 `install.sh`；私有 `releases/download` 不是免 token 入口。
- `verified_latest` 为 `null` 或 `latest` 为空的产品报告 `unavailable`，不猜版本。
- Scaena `v0.1.2` 的 `--version` build metadata 已知不准，不能当严格版本证据（见 `private-release-reference.md`）。

## 阶段 2 安装 skills

```bash
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-router --yes
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-bootstrap --yes
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-action-receipt --yes
npx --yes skills add https://github.com/yeisme/ai-drama-skills --skill ai-drama-remote-operations --yes
npx --yes skills add https://github.com/yeisme/scaena-skills --skill scaena-asset-draw-batch --yes
npx --yes skills add https://github.com/yeisme/scaena-skills --skill scaena-bounded-replacement --yes
eikona setup --yes --runtimes agents,codex
scaena setup auto 2>/dev/null || scaena skills install --runtimes auto --yes --agent
scaena skills doctor --agent
```

- `eikona setup` 只装 Eikona 自己的精确版本 skills lock，**不覆盖未管理 Skill 路径**；冲突时返回 `eikona skills plan`，不自动替换。
- `SKILLS_RELEASE_NOT_MIRRORED` → 报告缺口，临时用 `eikona setup --yes --skip-skills`，不声称装齐。
- 不向 `.codex/skills/` 重复安装同一 Skill；不从 runtime 副本发布源码。
- 聚合仓 `yeisme-agent-my-skills` 带嵌套 submodule，安装做剧 skill 时指向 `ai-drama-skills` / `scaena-skills`，不指向聚合仓。

## 阶段 3 连接

**client**

```bash
eikona remote connect --endpoint <EIKONA_ENDPOINT> --key-file <KEY_FILE_EIKONA> --allow-private-http --project <PROJECT>
scaena remote connect --endpoint <SCAENA_ENDPOINT> --key-file <KEY_FILE_SCAENA> --allow-private-http --project <PROJECT>
eikona remote doctor --agent
scaena remote doctor --json
eikona remote describe --agent
```

**owner**

```bash
eikona service access-key issue --name drama-cli --role operator --purpose cli-remote-v1 --ttl 720h --key-file <KEY_FILE_EIKONA>
eikona serve --addr 127.0.0.1:18080 --api-key-file <KEY_FILE_EIKONA>
scaena-api config init --mode gateway --config /absolute/private/scaena-gateway.yaml --api-key-file <KEY_FILE_SCAENA> --project-root /absolute/scaena-data --public-base-url http://<lan-ip>:<port>
scaena-api serve --config /absolute/private/scaena-gateway.yaml
```

profile 落点：`~/.eikona/remote-profile.json`（`eikona.remote_profile.v1`）、`~/.scaena/remote-profile.json`（`scaena.remote_profile.v1`），均 mode 0600，**只存 endpoint / key-file 绝对路径 / 明文 LAN 许可 / project**，不含 secret。覆盖路径可用 `EIKONA_REMOTE_PROFILE` / `SCAENA_REMOTE_PROFILE`。

`eikona config env --provider openai --agent` 只用于查看环境变量**名称与状态**，不收集值。`eikona setup` 不接受或存储 provider 凭据。

## 已知缺口（如实报告，不绕过）

- `scaena remote` v1 slice 只路由 `remote / upload / mcp / doctor / board`；`init` / `workflow run` / storyboard-video generation / export 返回 `REMOTE_PROFILE_UNSUPPORTED_COMMAND`。这是 typed action 路由缺口（C1），**不得**用 `--no-remote` 在客户端落 owner state。
- 远程 `edit` 参考图必须是 owner 服务端可解析的 `eikona://artifact/<handle>`，客户端绝对路径（如 `/var/folders/.../T/...`）在 provider 调用前必须拒绝。
- 私网明文 / operator-managed HTTP 的 readiness 必须把 TLS 与 production 标为 `degraded|blocked`。

## 阶段 4 交接

交给 `ai-drama-router`（唯一语义入口），带 `automation_profile` 与六阶段 stage_plan，详见聚合仓 `docs/drama-execution-kernel/automation-core.md`。bootstrap 不生成 `DramaRoutePlan`、不写剧本、不发起生成。
