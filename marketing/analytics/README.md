# マーケティングデータ保存ルール — おくすり味ナビ

## 保存頻度
月1回（月初に前月分を保存）

## 保存するデータ

### 1. Google Search Console（必須）
- **取得方法**: Search Console →「検索パフォーマンス」→ 期間を前月に設定 → 「エクスポート」→ CSV
- **ファイル名**: `search-console.csv`
- **確認すべき指標**: クリック数、表示回数、CTR、掲載順位（キーワード別）

### 2. X Analytics（必須）
- **取得方法**: X → 「もっと見る」→「Creator Studio」→「アナリティクス」→ エクスポート
- **ファイル名**: `x-analytics.csv`
- **確認すべき指標**: インプレッション、エンゲージメント率、フォロワー増減

### 3. note 統計（必須）
- **取得方法**: note → ダッシュボード → **CSV不可のため手動メモ**
- **ファイル名**: `note-stats.md`
- **記録する項目**:
```markdown
# note 統計 — YYYY年MM月

## 記事別PV
| 記事タイトル | PV | スキ | コメント |
|------------|:--:|:---:|:------:|
| クラリスドライシロップの飲ませ方 | XXX | XX | X |
| ... | ... | ... | ... |

## 全体
- 月間PV合計: XXX
- フォロワー数: XX（前月比 +X）
- 新規公開記事数: X本
```

### 4. Cloudflare Web Analytics（任意）
- **取得方法**: Cloudflare Dashboard → Web Analytics → スクリーンショット
- **ファイル名**: `cloudflare-screenshot.png`
- **確認すべき指標**: ユニークビジター数、ページビュー、国別アクセス

### 5. Google Analytics（任意・導入している場合）
- **取得方法**: GA4 → レポート → エクスポート → CSV
- **ファイル名**: `ga4-report.csv`

## フォルダ構成
```
analytics/
├── README.md（このファイル）
├── 2026-04/
│   ├── search-console.csv
│   ├── x-analytics.csv
│   ├── note-stats.md
│   └── cloudflare-screenshot.png（任意）
├── 2026-05/
│   └── ...
```

## 分析の依頼方法
データを保存したら、Claude Code に以下のように依頼する：
```
おくすり味ナビの先月のマーケティングデータを分析して。
改善アクションを提案して。
```
analytics/ フォルダのデータを自動で読み取って分析します。
