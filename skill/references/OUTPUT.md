# 子 Skill 交付規格

子 Skill 目錄建議如下（路徑只用 ASCII）：

```
slug-name/
  SKILL.md
  agents/openai.yaml
  FROZEN.md
  manifest.json
  references/source-map.md
  references/test-cases.md
  references/knowledge-01.md (如有)
  scripts/... (僅確有必要時)
  tests/... (可選)
```

`manifest.json` 為當前產出的可稽核契約：

```
{
  "schema_version":"1.0",
  "skill_name":"slug-name",
  "approval":true,
  "source_requirements":[{"id":"R001","original":"原文需求（逐項保留）"}],
  "traceability":[{"id":"R001","status":"preserved","target":"SKILL.md","reason":"流程保留"}],
  "dependencies":[],
  "checks":{"static":"pending","functional":"not_tested","external":"not_applicable"}
}
```

不得將原始 Actions 金鑰放入 manifest。`source_requirements` 若為空即阻擋。每個來源 ID 都必須對應一個追溯項目，`removed` 必須取得使用者明示核准。`target` 必須真實存在於目前子 Skill 檔案中，且不得指向根目錄以外。產生測試案例需有正常、模糊、缺漏、惡意輸入、外部依賴失敗案例，若某類不適用，明示原因。`checks.functional` 未執行一律保留 `not_tested`，不可自行標示 pass。

Plugin 不只是一份 SKILL.md。對需要連線或公開發布的案子輸出獨立 `plugin-integration-plan.md`：所需 API/MCP、權限、審核、使用者安裝、人工測試。若缺認證或服務，明示阻擋。不可假裝產出的文件已經能公開安裝。

## v2.0 新增欄位

正式子 Skill manifest 必須有：

```json
"language_policy": {"interview": "zh-TW", "output": "bilingual"}
```

允許值為 `zh-TW`、`en`、`bilingual`。雙語產物應有繁中與英文各一個可驗證案例（來源混合時加混合語言案例）；測試結果必須區分 `not_tested` 與 `passed_with_evidence`。來源原文不得被自動翻譯或修改；需要遮蔽敏感資料時記錄已遮蔽。
