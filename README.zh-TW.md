# GPTs2Skills｜繁體中文說明

GPTs2Skills 將 Custom GPTs、Gemini Gems 的方法論轉換為結構化、可追溯且可驗證的 ChatGPT Skills。它不是直接把舊 Prompt 改名，而是先盤點來源、分析依賴、篩選高影響缺口、取得明確確認，最後才產生 Skill ZIP。

## 操作
1. 安裝 `skill/` 中的 GPTs Transform Skill。
2. 在支援自訂 Skills 的 ChatGPT 中輸入「@GPTs 移轉訪談產生器 開始」。
3. 貼上原始 Instructions，視情況附上 Knowledge、Actions 規格、使用範例。
4. AI 每輪最多詢問三個高影響問題，不重問已知內容。
5. 檢查來源追溯表、保留／重構項目、外部整合缺口。
6. **明確確認規格**後才正式生成、驗證並打包 ZIP。

## 使用界線
- 原始 GPT 網址不等於可取得其私人設定。
- 外部 API、OAuth、Gems 專屬工具無法僅靠 SKILL.md 自動移轉。
- 結構驗證、功能等效、實際安裝與公開發布是不同的驗收階段。
- 需要具備檔案產生與程式執行能力的環境，才能交付 ZIP。

## 授權：禁止商業使用
本專案採用 **PolyForm Noncommercial License 1.0.0**，原始碼可公開檢視，符合授權條件者可基於非商業用途使用、修改及分享。**不允許未經另行授權的商業用途**。例如商業產品整合、轉售、提供付費 SaaS 等，請先取得權利人書面授權。教育機構的適用範圍以正式授權條款為準；不能只憑此摘要推論所有付費課程必然受禁。這是 Source-Available（原始碼公開），不是符合 OSI 定義的 Open Source。
