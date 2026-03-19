- [x] Phase 1 Analyst: kusuri-navi.html の表示不具合と原因候補を特定する
- [x] Phase 2 Critic: 原因仮説を反証し、関連する副作用を確認する
- [x] Phase 3 Implementer: 最小変更で表示不具合と関連バグを修正する
- [x] Phase 4 Reviewer: 差分と動作を確認し、レビューと改善提案を tasks/todo.md に追記する

## Review
- Root cause: sticky 要素の `top` が `56px` 固定で、実際のヘッダー高さとズレるため、飲み合わせ表ヘッダーと先頭行が重なりやすかった。
- Related bug: 一覧タブのクリック処理が `.filter-tab` 全体を対象にしており、飲み合わせ表側の active 状態まで巻き込んでいた。
- Fix: ヘッダー実寸を `updateStickyMetrics()` で CSS 変数へ反映し、一覧検索欄と表ヘッダーの sticky offset を共通管理に変更した。
- Fix: 一覧遷移時にカードが sticky ヘッダー配下へ隠れないよう `scroll-margin-top` を追加した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Risk: 実ブラウザでの描画確認は未実施。端末依存のフォント差分や Safari 固有挙動は目視確認が残る。
- Improvement ideas:
  - `viewport` の `user-scalable=no` はアクセシビリティ上の不利が大きいので外す。
  - データ量が増えるなら `renderCard()` の文字列連結をテンプレート分割して保守性を上げる。
  - 飲み合わせ表に「先頭列固定中」の視覚ヒントを足すと横スクロール時の理解が上がる。

## Follow-up Review
- Change: `viewport` から `user-scalable=no` を削除し、拡大操作を許可した。
- Change: 飲み合わせ表の凡例下に、左列固定と横スクロールを説明するヒントを追加した。
- Change: `renderCard()` を味・GE・混ぜ物・注意の小関数へ分割し、HTML 文字列の責務を整理した。
- Test: `python3 tests/kusuri_navi_regression_check.py`

## Visual Review
- Change: ブランドカラーを紫系から明るいティール系へ変更し、薬剤師向けの清潔感と保護者向けの柔らかさを両立する方向に寄せた。
- Change: 表ヘッダーにグラデーションと影を追加し、固定列にも影を入れて横スクロール時の境界を見やすくした。
- Test: `python3 tests/kusuri_navi_regression_check.py`

## Card Review
- Change: 閉じたカードでも `おすすめ / まあまあ / NG` 件数と代表的なおすすめ候補が分かる相性サマリーを追加した。
- Change: 一覧カードから `散剤` バッジを削除し、漢方のみラベルを残した。
- Change: お気に入りはハート記号へ統一し、閉じたカード右上から直接押せるようにした。
- Test: `python3 tests/kusuri_navi_regression_check.py`

## Maker Review
- Change: 閉じたカードの相性サマリーは件数表示から、おすすめ上位2候補のアイコン中心表示へ切り替えた。
- Change: メーカーフィルター上の `ツムラ(XX)` は `ツムラ` に統一し、絞り込みも統一表記で動くようにした。
- Change: 漢方番号は閉じたカードの薬品名横に `ツムラ XX` として残した。
- Test: `python3 tests/kusuri_navi_regression_check.py`

## Drug Data Review
- Change: 対象外剤形の `ホクナリンテープ` と `デカドロンエリキシル` を一覧から除外した。
- Change: 対象薬として `ビオスリー配合散`、`麻杏甘石湯`、`桔梗湯`、`桂枝加芍薬大黄湯` を追加した。
- Change: 今回の検証はまず「散剤・漢方という対象剤形に合っているか」を中心に見直した。
- Change: 抗てんかん薬 3剤の分類を `かぜ薬` から `けいれん・神経系` に修正した。
- Test: `python3 tests/kusuri_navi_regression_check.py`

## Pharmacist Review Plan
- [x] Phase 1 Analyst: 公開画面と内部レビューの導線を分け、未監修データをどこで止めるかを設計する
- [x] Phase 2 Critic: 「未監修を隠す」だけでは壊れる導線（一覧0件、メーカー絞り込み、お気に入り、表遷移）を洗い出す
- [x] Phase 3 Implementer: 各薬に監修メタデータを持たせ、公開判定を一箇所へ集約する
- [x] Phase 3 Implementer: 監修チェック用の一覧表を自動生成し、内部向けにCSV出力できるようにする
- [x] Phase 3 Implementer: 薬剤師監修レビューシートのテンプレートを追加する
- [x] Phase 4 Reviewer: 公開画面に未監修データが出ないこと、レビュー用一覧が全薬を拾うこと、回帰チェックが通ることを確認する

## Pharmacist Review Spec
- Public rule: `review.verified === true` かつ `review.verifiedOn` が入っている薬のみ公開画面に表示する
- Internal rule: 監修一覧は全薬を対象にし、`verified / pending / needs_revision` の状態、確認日、監修者、根拠、メモを確認できるようにする
- Data rule: 各薬は `review` オブジェクトを必ず持ち、未設定時は安全側のデフォルトで補完する
- UX rule: 公開中の監修済み薬が 0 件でも「壊れている」と誤解されない説明文を出す
- Risk note: 現状は正式監修前のため、初期データは公開対象 0 件を許容する

## Pharmacist Review Result
- Change: 全薬に `review` メタデータを付与し、初期状態は `verified: false` / `verifiedOn: ""` / `status: "pending"` で統一した。
- Change: 一覧・飲み合わせ表・お気に入り・メーカー絞り込みは `getPublicMedicines()` 経由へ寄せ、未監修データを公開画面から除外した。
- Change: 監修済み公開件数と非表示ポリシーを各ページの注記に出し、公開件数 0 件でも壊れて見えないようにした。
- Change: `?review=1` または `#review` で内部用の監修ページを表示し、全薬の監修状態一覧と CSV 出力を自動生成できるようにした。
- Change: 手入力用の雛形として `tasks/pharmacist_review_sheet_template.csv` を追加した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node` / `jsc` がないため、JS エンジンによる構文チェックまでは未実施。
- Risk: `review mode` は画面上の分離のみで、認証や配布制御ではない。公開アプリで内部一覧を完全に隠すには別途アクセス制御が必要。

## Low-risk NCCHD Design Plan
- [x] Phase 1 Analyst: NCCHD資料のどこまでを一次情報として使い、どこから先を推測扱いにするか整理する
- [x] Phase 2 Critic: 「公式資料ベースなら安全」という思い込みを崩し、転載・表現・未掲載薬の扱いのリスクを洗い出す
- [x] Phase 3 Implementer: 低リスク版の設計書を作成し、公開範囲・画面仕様・データモデル・運用ルールを定義する
- [x] Phase 4 Reviewer: 実装着手前の判断材料として、仕様がMVP・法務・監修運用の3点を満たすか確認する

## Low-risk NCCHD Design Review
- Decision: 初期公開は `NCCHD PDF に掲載された薬だけ` に限定し、未掲載薬は推測で補完しない方針にした。
- Decision: 画面文言は `おすすめ / NG` から、資料準拠の `飲みやすい / 変わらない / 飲みにくい / データなし` へ寄せる設計にした。
- Decision: AI は公開文言生成には使わず、検索補助や入力ゆれ吸収に限定する設計にした。
- Decision: `監修` は別レイヤーとし、将来追加する場合も `公的資料掲載` と `薬剤師確認済み追加` を混在表示しない方針にした。
- Artifact: `tasks/low_risk_ncchd_mvp_design.md`
- Risk: NCCHD PDF 自体に別媒体からの抜粋表記があるため、転載範囲や表現の仕方は公開前に再確認が必要。

## Low-risk NCCHD Implementation Plan
- [x] Phase 1 Analyst: NCCHD掲載薬のうち現行データでそのまま公開できるものと、名称補正が必要なものを分ける
- [x] Phase 2 Critic: 現行の評価軸・表カラム・自由記述が公式資料とズレる箇所を洗い出す
- [x] Phase 3 Implementer: 公開画面をNCCHD掲載薬だけに切り替え、評価文言と出典表示を資料準拠へ更新する
- [x] Phase 4 Reviewer: 一覧・表・凡例・詳細が公式資料ベースで一貫していることを確認する

## Low-risk NCCHD Implementation Review
- Change: NCCHD PDF の行列を `officialSourceMap` として実装し、掲載薬 18件だけを公開対象にした。
- Change: `isPublicMed` は `公的資料掲載` または `薬剤師確認済み追加` に限定し、未掲載薬は内部に残したまま公開画面から除外した。
- Change: 一覧の凡例、カード要約、飲み合わせ表の列を `飲みやすい / 変わらない / 飲みにくい / データなし` と NCCHD の列順に合わせた。
- Change: カードでは自由記述より `味・香り・出典` を優先表示し、詳細にも NCCHD PDF へのリンクを出すようにした。
- Change: 現行データに無かった `セファクロル細粒` を追加し、NCCHD掲載薬の抜けを 1件補完した。
- Source: `https://www.ncchd.go.jp/hospital/about/section/medicine/210330.html`
- Source: `https://www.ncchd.go.jp/hospital/about/section/medicine/nomiawase.pdf`
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Risk: 実ブラウザでの目視確認は未実施。カテゴリタブに `漢方` など未掲載カテゴリが残っているため、次段で公開対象に応じた動的タブ化を検討する。

## Low-risk NCCHD Continuation Plan
- [x] Phase 1 Analyst: 固定カテゴリタブと公開対象レイヤーのズレを整理する
- [x] Phase 2 Critic: 公開対象だけに絞ったとき、タブ・検索・レビュー一覧で破綻する箇所を洗い出す
- [x] Phase 3 Implementer: official / reviewed / internal の層を関数化し、タブを公開対象から動的生成する
- [x] Phase 4 Reviewer: 公開画面に未掲載カテゴリが出ないこと、レビュー一覧で3層が識別できることを確認する

## Low-risk NCCHD Continuation Review
- Change: 一覧タブと飲み合わせ表タブを固定HTMLから空コンテナに変え、公開対象から `renderCategoryTabs()` / `renderTableFilterTabs()` で動的生成するようにした。
- Change: データ参照は `getOfficialMedicines()` / `getReviewedExtensions()` / `getInternalCandidates()` に分離し、公開・追加・内部候補の3層をコード上でも明示した。
- Change: 検索対象は表示名・味・香り・メーカーラベルベースへ寄せ、公式掲載名でも見つかるようにした。
- Change: 監修一覧では `公的資料 / 追加薬 / 非公開` を識別できるまま、公開件数サマリーも3層前提に更新した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Risk: 動的タブ化により、公開対象が少ない時は絞り込みの選択肢が減る。もし教育用途で全カテゴリを常に見せたいなら、別の説明UIが必要。

## Internal Candidate Review Plan
- [x] Phase 1 Analyst: 監修ページで公開薬と内部候補が混ざる問題を整理する
- [x] Phase 2 Critic: CSVだけで済ませず、画面上でも内部候補の優先順位が分かる構成を定義する
- [x] Phase 3 Implementer: 監修ページを `公的資料掲載 / 監修済み追加 / 内部候補` の3セクションへ分割する
- [x] Phase 3 Implementer: CSVにレイヤー列を追加し、内部候補の抽出条件を明示する
- [x] Phase 4 Reviewer: 監修ページとCSVの両方で3層が整合していることを確認する

## Internal Candidate Review Result
- Change: 監修ページの単一テーブルを廃止し、`公的資料掲載 / 監修済み追加 / 内部候補` の3セクションへ分割した。
- Change: 各セクションは件数つきの見出しと独立テーブルを持ち、空セクションでも「対象データはありません」と明示するようにした。
- Change: レビューCSVに `レイヤー` 列を追加し、`official / reviewed / internal` をエクスポートできるようにした。
- Change: 画面表示とCSVのレイヤー判定は `getReviewSheetRows()` の `layer` フィールドに集約した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Risk: 監修ページの情報量は増えたため、将来的に件数がさらに増えるならセクションごとの検索や折りたたみを検討してよい。

## Review Workflow Redesign Plan
- [x] Phase 1 Analyst: CSV入力を廃止した前提で、監修ページだけに残すべき操作と監査ログ要件を整理する
- [x] Phase 2 Critic: 単一入力経路でも起こる事故（誤承認、なりすまし、同時編集、公開前漏れ）を洗い出す
- [x] Phase 3 Implementer: 監修ページ入力前提のシンプルかつ堅牢な監修フロー設計書を作成する
- [x] Phase 4 Reviewer: フローが `入力経路1つ / セキュリティ考慮 / 実務運用可能` の3条件を満たすか確認する

## Review Workflow Redesign Result
- Decision: 監修入力は監修ページだけに統一し、CSVはエクスポート専用とする方針にした。
- Decision: 状態は `internal_candidate / editing / review_ready / approved / published / rejected` の6段階に整理した。
- Decision: 単一入力経路でも事故を防ぐため、`approved` と `published` を分離し、公開は別ロールまたは別操作にした。
- Decision: セキュリティ面では、監修ページを本番公開アプリから分離し、認証・2FA・RBAC・監査ログ・楽観ロックを必須とした。
- Artifact: `tasks/review_page_only_workflow.md`
- Risk: 現在の `#review` / `?review=1` は運用確認には使えても、本番の監修入力画面としては不十分。将来的な管理画面分離が前提になる。

## Review Workflow UI Plan
- [x] Phase 1 Analyst: 現行レビュー画面で入力に必要な最小項目と、公開判定に効く状態遷移を整理する
- [x] Phase 2 Critic: ブラウザ内保存で起こる事故（誤公開、下書きの公開残り、監査ログ欠落）を洗い出す
- [x] Phase 3 Implementer: 監修ページに単一入力フォーム、状態遷移ボタン、監査ログ表示を実装する
- [x] Phase 3 Implementer: 公開条件を `published` に厳格化し、CSVにワークフロー情報を出力する
- [x] Phase 4 Reviewer: 監修ページから保存・承認・公開まで辿れること、未公開データが公開画面へ出ないことを確認する

## Review Workflow UI Result
- Change: 監修ページに `reviewEditor / reviewAudit` を追加し、一覧から選んだ薬だけを単一入力フォームで扱えるようにした。
- Change: 追加薬の状態は `internal_candidate / editing / review_ready / approved / published / rejected` で保持し、公開画面は `published` のみ通すようにした。
- Change: 監修入力は `localStorage` に保存し、操作ごとに append-only 風の監査ログと `version` を残すようにした。
- Change: 公式掲載薬は監修ページで参照専用にし、追加薬だけが `保存 -> 確認待ち -> 承認 -> 公開` を通るようにした。
- Change: CSV 出力に `workflowStatus / 公開日 / 操作者 / 最終更新 / version` を追加し、監査資料として追いやすくした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Risk: この実装はローカルブラウザ保存なので、本番の認証・権限制御・改ざん防止にはならない。管理画面分離とサーバー保存は別途必要。

## Subjective Review Input Plan
- [x] Phase 1 Analyst: 味・香り・相性・注意事項が公開UIのどこに効いているかを整理する
- [x] Phase 2 Critic: 主観項目を別の正本にせず、レビュー保存データから公開UIへ一貫反映する方法を定義する
- [x] Phase 3 Implementer: 監修ページに主観項目の入力欄を追加し、review record へ保存する
- [x] Phase 3 Implementer: 主観項目を一覧・カード・表・CSVへ反映し、確認待ち前の必須項目に組み込む
- [x] Phase 4 Reviewer: 入力した主観項目が保存後のプレビューと公開表示へ反映されることを確認する

## Subjective Review Input Result
- Change: 追加薬の review record に `subjectiveTasteTags / subjectiveTasteDetail / subjectiveFlavor / subjectiveCaution / subjectiveCompat` を追加し、主観項目の正本を監修保存データへ寄せた。
- Change: 監修ページに味タグ、味の詳細、香り、注意事項、相性マトリクスの入力欄を追加し、`保存 / 確認待ち / 承認 / 公開` の各遷移で同じ入力値を使い回せるようにした。
- Change: `syncMedicineReviews()` で主観項目を `med` へ戻し込み、一覧カード・詳細・飲み合わせ表・検索・CSV が同じ値を参照するようにした。
- Change: `review_ready / approved / published` 前には、味情報・香り・相性マトリクスの最低入力を必須化した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Risk: 主観項目は静的HTML上では誰がどの根拠で入力したかを完全には縛れない。正式運用では監修ロールとサーバー保存が必要。

## Taste Normalization Plan
- [x] Phase 1 Analyst: 味タグの自由選択がどこで表現ぶれを起こすかを整理する
- [x] Phase 2 Critic: 既存の `subjectiveTasteTags` を壊さず、正規化された味入力へ移行する方法を決める
- [x] Phase 3 Implementer: 監修ページの味入力を `主な味 / 副次的な味 / 後味` に変更し、タグは自動生成する
- [x] Phase 3 Implementer: CSV と監査差分に正規化項目を追加し、公開表示が同じ味ラベルを使うようにする
- [x] Phase 4 Reviewer: 既存データを維持しつつ、新入力が一覧・カード・CSVへ反映されることを確認する

## Taste Normalization Result
- Change: 主観味データに `subjectiveTastePrimary / subjectiveTasteSecondary / subjectiveTasteAftertaste` を追加し、味タグはその3項目から自動生成するようにした。
- Change: 旧 `subjectiveTasteTags` だけを持つ保存データも読み込み時に正規化項目へ吸い上げ、既存データを壊さず移行できるようにした。
- Change: 監修ページの味入力はチェックボックスから `主な味 / 副次的な味 / 後味` の選択式へ変更し、表現ぶれを抑えた。
- Change: CSV に `主な味 / 副次的な味 / 後味` を追加し、監査時にも正規化された味情報を確認できるようにした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Risk: 旧データの3個目以降の味タグは `後味` へ寄せて解釈しているため、厳密な意味づけが必要な場合は初回レビュー時に見直しが必要。

## Flavor Normalization Plan
- [x] Phase 1 Analyst: 現行の香り自由入力がどこで表現ぶれを起こすかを整理する
- [x] Phase 2 Critic: 旧 `subjectiveFlavor` を壊さず、正規化された香り入力へ移行する方法を決める
- [x] Phase 3 Implementer: 監修ページの香り入力を `主な香り / 副次的な香り / 香りの詳細` に変更し、表示ラベルを自動生成する
- [x] Phase 3 Implementer: CSV と監査差分に正規化項目を追加し、公開表示が同じ香りラベルを使うようにする
- [x] Phase 4 Reviewer: 既存データを維持しつつ、新入力が一覧・カード・CSVへ反映されることを確認する

## Flavor Normalization Result
- Change: 主観香りデータに `subjectiveFlavorPrimary / subjectiveFlavorSecondary / subjectiveFlavorDetail` を追加し、公開表示用の `subjectiveFlavor` はそこから自動生成するようにした。
- Change: 旧 `subjectiveFlavor` の自由入力は読み込み時に正規化キーへ変換し、既存データも壊さず移行できるようにした。未解釈の値は `その他 + 詳細` として保持する。
- Change: 監修ページの香り入力は自由入力から `主な香り / 副次的な香り / 香りの詳細` へ変更し、無香料や漢方特有も選択肢で扱えるようにした。
- Change: CSV に `主な香り / 副次的な香り / 香りの詳細 / 香り表示` を追加し、監査時にも正規化済みの香り情報を確認できるようにした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Risk: 旧香り文字列からの自動解釈はキーワードベースなので、曖昧な表現は初回レビュー時に見直しが必要。

## List Table Memo Plan
- [x] Phase 1 Analyst: 一覧・表・お気に入り・メモ導線の現状を整理し、ユーザー要望8点の影響範囲を切り分ける
- [x] Phase 2 Critic: メモ保存、表ポップアップ、一覧/表件数整合で起きる副作用を洗い出す
- [x] Phase 3 Implementer: カードUI、凡例位置、ハート配置、ポップアップ、メモ機能、メモタブを実装する
- [x] Phase 3 Implementer: 一覧フィルターと表フッターを調整し、一覧/表の母数が同じになるよう統一する
- [x] Phase 4 Reviewer: メモ付き薬だけがメモタブに出ること、表からポップアップが開くこと、一覧/表の基準データが揃うことを確認する

## List Table Memo Result
- Change: 展開済みカード内のハートを削除し、閉じたカード右上のハートだけを残した。
- Change: `資料上の相性` の凡例をカード詳細のラベル横へ移し、一覧上部の凡例表示はなくした。
- Change: 端末ローカル保存のメモ欄を各薬カードと表ポップアップに追加し、`メモ` タブではメモ記入済みの公開薬だけを表示するようにした。
- Change: 飲み合わせ表の薬名クリックは一覧遷移をやめ、同一画面上のポップアップ詳細表示へ切り替えた。
- Change: 一覧と表のカテゴリ絞り込みを `filterByPublicCategory()` に統一し、表にも件数表示を追加して公開母集団のズレを避けた。
- Change: 一覧と表の件数表示を `公開母数` 基準に統一し、絞り込み時は `表示 n件 / 公開母数 m件` と出すようにした。
- Change: 検索欄の自動復元で初期件数がぶれにくいよう、初期化時に検索入力をクリアし `autocomplete=\"off\"` を付けた。
- Change: 一覧フィルターから `散剤` を外し、飲み合わせ表フッターにも出典リンクを追加した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: 簡易 Node ハーネスで `getPublicMedicines().length === getTableMeds().length === 18` と ID 順一致を確認
- Risk: ブラウザ実機での最終確認は未実施。ポップアップ内のスクロール量とメモ入力時の体感は Safari / iPhone で一度確認が必要。

## Table First Rows Bug Plan
- [x] Phase 1 Analyst: 飲み合わせ表の先頭2行が見えない原因を、データ欠落・描画順・スクロール位置の3系統で切り分ける
- [x] Phase 2 Critic: 行高や sticky 設定だけを疑う見立てに穴がないか確認する
- [x] Phase 3 Implementer: 最小変更で、ページ切替直後でも表の先頭行が必ず見えるようにする
- [x] Phase 4 Reviewer: 先頭2行が隠れないことと、他ページ遷移の副作用がないことを確認する

## Table First Rows Bug Result
- Root cause: ワイドシリン・クラリスが欠落していたのではなく、実ブラウザでは飲み合わせ表ヘッダーの縦 sticky が先頭2行を覆っていた。ページ切替時のスクロール持ち越しも見え方を悪化させていた。
- Critic check: データ件数・描画件数・表行数はいずれも 18 件で一致しており、データ欠落や並び順は原因ではなかった。
- Change: `resetPageScroll()` を追加してページ切替後のスクロール位置を初期化しつつ、飲み合わせ表ヘッダーの縦 sticky を外して先頭行が覆われないようにした。横比較用の左列 sticky は維持した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: 簡易 Node ハーネスで `setCurrentPage('page-table')` 実行後に `window.scrollTo` と `page-table.scrollIntoView` が呼ばれ、`document.documentElement.scrollTop` と `document.body.scrollTop` が 0 になることを確認

## Popup Memo Fav Plan
- [x] Phase 1 Analyst: ポップアップ、メモタブ、お気に入りタブのカード挙動と編集導線を整理する
- [x] Phase 2 Critic: ハート状態同期、メモ編集、カード初期展開の競合を洗い出す
- [x] Phase 3 Implementer: ポップアップにハートを追加し、メモ/お気に入りタブのカードを初期展開で編集可能にする
- [x] Phase 4 Reviewer: ハート同期とメモ編集の回帰を確認する
- [x] UX Proposal: 子連れ母と薬剤師にとっての最適なタブ構成案をまとめる

## Popup Memo Fav Result
- Change: 飲み合わせ表のポップアップにもハートを追加し、カード側と同じ `data-fav-id` で状態同期するようにした。
- Change: メモタブのカードは初期表示で展開した状態にし、メモ欄をそのまま編集できるようにした。
- Change: お気に入りタブのカードも初期表示で展開し、メモ欄を直接編集できるようにした。メモがある薬はプレビューも残した。
- Change: タブ構成の提案としては、薬剤師の即答用途を優先して `一覧 / 飲み合わせ表 / 保存` の3本を基本とし、`保存` 内で `お気に入り / メモあり` を切り替える案が最も重複が少ないと判断した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`

## Multi Med Density Plan
- [x] Phase 1 Analyst: 複数薬まとめの切替UIと候補カードが視認性を落としている箇所を整理する
- [x] Phase 2 Critic: 目立たせるだけで横幅が増えすぎないか、詳細折りたたみとの相性を確認する
- [x] Phase 3 Implementer: モード切替をスライド式セグメントへ変更し、候補カードを3列グリッド基準へ詰める
- [x] Phase 4 Reviewer: 回帰チェックを更新し、既存の複数薬まとめ導線が壊れていないことを確認する

## Multi Med Density Result
- Change: `単剤表示 / 複数薬まとめ` を `data-active-mode` とスライドサム付きのセグメントUIへ変更し、表タブ内で切替の存在に気づきやすくした。
- Change: 複数薬まとめの候補カードは1列表示をやめ、3列グリッドへ変更した。4件目以降は自動で2行目以降へ回る。
- Change: カード見出しの余白と文字サイズを詰め、詳細は既存の折りたたみ前提のまま一覧性を優先した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`
- Test: 簡易 Node ハーネスで、メモ/お気に入りカードが `open` で描画され、ポップアップにハートとメモ欄が入ることを確認

## Saved Tab Consolidation Plan
- [x] Phase 1 Analyst: 既存のメモ/お気に入りページと下部ナビの依存箇所を整理し、統合対象を確定する
- [x] Phase 2 Critic: 保存済み統合でメモ編集、ハート同期、空状態表示が壊れないか確認する
- [x] Phase 3 Implementer: `保存済み` ページと内部フィルター `すべて / お気に入り / メモあり` を実装する
- [x] Phase 4 Reviewer: 回帰チェックを更新し、3タブ構成で保存済みフィルターが機能することを確認する

## Saved Tab Consolidation Result
- Change: 下部ナビを `一覧 / 飲み合わせ表 / 保存済み` の3タブに整理し、`メモ` と `お気に入り` の別タブを `保存済み` へ統合した。
- Change: `保存済み` ページの内部フィルターとして `すべて / お気に入り / メモあり` を追加し、同じカードUIのまま切り替えられるようにした。
- Change: 保存済みページのカードは初期展開状態で、ハート操作とメモ直接編集の両方をその場で行えるようにした。
- Change: 保存済みページの注記は、お気に入りとメモの非公開件数をまとめて案内する形にした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: 簡易 Node ハーネスで `お気に入り` フィルターはワイドシリンのみ、`メモあり` フィルターはクラリスのみ表示されることを確認

## Saved Card Memo Plan
- [x] Phase 1 Analyst: 保存済みページのカード構造を見直し、閉じた状態のままメモ欄だけ常時表示する差し込み位置を決める
- [x] Phase 2 Critic: メモ編集中の誤開閉や、他ページのカード表示への副作用がないか確認する
- [x] Phase 3 Implementer: 保存済みサマリーを追加し、閉じたカード + 外出しメモ編集へ変更する
- [x] Phase 4 Reviewer: 回帰チェックを更新し、保存済みページの表示とメモ編集が維持されることを確認する

## Saved Card Memo Result
- Change: 保存済みページの上部に `保存済み / お気に入り / メモあり` の小サマリーを追加した。
- Change: 保存済みページの薬カードは閉じた状態に戻し、詳細とは別に外出しのメモ欄を常時表示して、カードを開かずに直接編集できるようにした。
- Change: 一覧や飲み合わせ表のカード挙動は変えず、保存済みページだけ `showInlineMemoEditor` を使う形にして副作用を抑えた。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: 簡易 Node ハーネスで、保存済みカードが初期状態で閉じており、外出しメモ欄とサマリーが表示されることを確認

## Table Save Columns Plan
- [x] Phase 1 Analyst: 飲み合わせ表レンダリングと保存系イベントの接点を整理し、列追加の影響範囲を確定する
- [x] Phase 2 Critic: スマホ横幅、ポップアップ導線、既存メモ同期への副作用を洗い出す
- [x] Phase 3 Implementer: 飲み合わせ表にお気に入り列とメモ列を追加し、直接編集可能にする
- [x] Phase 4 Reviewer: 回帰チェックを更新し、表からのハート操作とメモ編集が維持されることを確認する

## Table Save Columns Result
- Change: 飲み合わせ表の `商品名` の右に `保存` 列と `メモ` 列を追加し、ハート操作とメモ編集を表から直接できるようにした。
- Change: スマホ横幅を考慮して、保存列は細く、メモ列は 170px 程度に抑え、既存の横スクロール前提で破綻しない幅にした。
- Change: 既存の `handleFav()` と `.memo-textarea` のイベントを再利用し、表・カード・ポップアップで状態が揃うようにした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: 簡易 Node ハーネスで、飲み合わせ表の HTML に `保存` ヘッダー、`メモ` ヘッダー、ハートボタン、メモ textarea が入ることを確認

## Table Header Icon Plan
- [x] Phase 1 Analyst: 表ヘッダーの sticky 条件、列順、保存済みナビアイコンの実装位置を確認する
- [x] Phase 2 Critic: ヘッダー固定を戻しても先頭行欠けが再発しない条件を整理する
- [x] Phase 3 Implementer: 表ヘッダー固定、`お気に入り` 列名、メモ列右移動、保存済み星アイコンを実装する
- [x] Phase 4 Reviewer: 回帰チェックを更新し、実機要望が反映されていることを確認する

## Table Header Icon Result
- Change: iPhone Safari で効きにくい `thead th` の sticky をやめ、表示用ヘッダーを `compatStickyHead` に分離して固定する形へ切り替えた。下へスクロールしても `ココア / プリン` などの列名が残る。
- Change: 表の `保存` 列名を `お気に入り` に変更した。
- Change: 表の `メモ` 列を右端へ移動し、左側は `商品名 / お気に入り / 味 / 香り` を優先表示する並びにした。
- Change: `保存済み` タブの下部ナビアイコンをハートから星へ変更し、お気に入りハートとの混同を避けた。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: 固定ヘッダーの専用ラッパー、`お気に入り` ヘッダー、右端 `メモ` 列、保存済みナビの星アイコンが回帰チェックに通ることを確認

## Table Header Follow-up Result
- Change: 固定ヘッダーと1行目の間に出ていた白い空白を、`compatStickyHead` の高さぶんを負マージンで打ち消す形で解消した。
- Change: 横向き時の `味` 列以降のズレを防ぐため、元テーブルの各ヘッダー実測幅を固定ヘッダー側へ同期する処理を `syncCompatStickyHead()` に追加した。
- Change: 横スクロール時に `種類` と `商品名` が流れないよう、本文と固定ヘッダーの両方で 2 列 sticky にし、`商品名` の left を `種類` 列の実測幅に追従させた。
- Change: 固定ヘッダーの横同期は `transform` をやめ、`compatStickyHead.scrollLeft = wrap.scrollLeft` に切り替えた。これで左固定列を残したまま残りの列だけ横移動する。
- Risk: 列幅同期は実測値ベースなので、フォントやブラウザ差には比較的強いが、将来セル構造を変えた場合は `syncCompatStickyHead()` の幅コピー対象を見直す必要がある。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`

## Card Summary NG Result
- Change: 一覧カードの相性サマリーを `飲みやすい` 最大3件に拡張し、`NG` 最大2件を同じカードヘッダー内へ常時表示するようにした。
- Change: `summary-label-bad` と `summary-pick-bad` を追加し、既存の明るい配色を崩さず NG を赤系ピルで識別できるようにした。
- Change: NG がある場合だけ2段目に出し、`mixGood` も `mixBad` もない薬は従来どおり「飲みやすい組み合わせの記載はありません」を表示する。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`

## Disclaimer Footer Result
- Change: ヘッダー直下に免責バナーを追加し、医療行為の代替ではないことと最終判断の確認先を起動直後に見えるようにした。
- Change: 免責バナーは通常フロー表示にし、`×` ボタンでその場だけ閉じられるようにした。sticky にはせず、既存の検索欄やヘッダーの固定挙動とは干渉させていない。
- Change: `page-list`、`page-table`、`page-saved` のフッターを統一し、`最終データ更新: 2025年6月`、出典リンク、免責、服薬上の注意を同じ形で表示するようにした。
- Change: `page-review` の内部向けフッターは変更していない。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`

## Public Rule Copy Result
- Change: `公開ルール` の文言を簡素化し、件数や非公開内訳を出さず「国立成育医療研究センター公開資料の掲載薬だけを表示しています。」だけを表示するようにした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`

## PWA Result
- Change: `kusuri-navi.html` を `index.html` にリネームし、Cloudflare Pages でルート配信しやすい構成へ切り替えた。
- Change: `manifest.json` と `sw.js` を追加し、`index.html` に PWA 用メタタグと Service Worker 登録を追加した。
- Change: `icons/` ディレクトリと `icon-192.png` / `icon-512.png` のプレースホルダーファイルを追加した。
- Risk: アイコンは空プレースホルダーのため、実機のインストール導線や Lighthouse の一部警告は、実画像配置後に最終確認が必要。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## IOS UI Filter Result
- Change: タイトル表記を `おくすり味ナビ` に統一し、`<title>`、ヘッダー、PWA の Apple タイトル、manifest 名称を揃えた。
- Change: iPhone で下部ナビがホームジェスチャーと干渉しにくいよう、ナビを少し浮かせて余白と角丸を追加した。
- Change: 飲み合わせ表のメモ欄高さを詰めて、1画面に入る行数を増やした。
- Change: `ペリアクチン`、`シングレア`、`オノンドライシロップ` のカテゴリ誤分類を修正し、`抗アレルギー` と `気管支` フィルターの表示を実際の期待に合わせた。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## PWA Title Result
- Change: ホーム画面追加時の表示名が短縮されないよう、`apple-mobile-web-app-title` と manifest の `short_name` を `おくすり味ナビ` に揃えた。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## IOS Install Name Follow-up Result
- Change: iOS の「ホーム画面に追加」ダイアログで名称ソースが分かれても揃うよう、`application-name` を追加し、初期化時に `document.title` も `おくすり味ナビ` へ正規化するようにした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## GitHub Push Plan
- [ ] Phase 1 Analyst: ローカルフォルダの Git 状態とファイル一覧を確認し、初期化が必要か判断する
- [ ] Phase 2 Critic: 既存 GitHub リポジトリへの上書きリスクを確認し、安全な push 方針を決める
- [ ] Phase 3 Implementer: ローカル初期化、コミット、リモート接続、push を実行する
- [ ] Phase 4 Reviewer: push 結果と現在のブランチ/リモート状態を確認する

## Multi Med Summary Plan
- [x] Phase 1 Analyst: 飲み合わせ表の既存構造と sticky テーブル制約を確認し、複数薬まとめUIの差し込み位置を決める
- [x] Phase 2 Critic: 行選択、横スクロール、カテゴリ切替、表ヘッダー固定への副作用を洗い出す
- [x] Phase 3 Implementer: `単剤表示 / 複数薬まとめ` 切替、薬選択UI、共通候補サマリーを表タブ内に実装する
- [x] Phase 4 Reviewer: 回帰チェックを更新し、既存表機能を壊さず集計ルールが反映されることを確認する

## Multi Med Summary Result
- Change: 飲み合わせ表タブ内に `単剤表示 / 複数薬まとめ` 切替を追加し、上位タブは増やさずに複数薬集計へ入れるようにした。
- Change: 複数薬まとめ時は薬名セル内のチェックで選択できるようにし、横幅を増やさず既存の表導線を保った。
- Change: 選択した薬に対して、`✅ すべてに飲みやすい`、`▲ まあまあ / 概ね問題なし`、`⚠ いずれかでNG` を `getCompatEntries()` ベースで集計するサマリーを追加した。
- Change: 集計ルールは、全薬 `G` を緑、`B` なし + 少なくとも1薬 `G/O` をグレー、1薬でも `B` を含むものを赤として扱い、薬ごとの評価メモも表示する。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Multi Med Summary Follow-up Result
- Change: `単剤表示 / 複数薬まとめ` セレクタは絵文字付きの強いピルUIに変え、表タブ内で見つけやすくした。
- Change: 選択済み薬はピル表示にし、`×` ボタンから1件ずつ解除できるようにした。
- Change: 緑/グレー/赤の各グループ詳細は折りたたみ可能にし、初期状態ではタイトル一覧を優先して1画面に収まりやすくした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Copy Cleanup Result
- Change: カード要約、ポップアップ、複数薬まとめを含む相性文言から `資料上:` の接頭辞を削除し、表示を簡潔にした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Table Mode Color Result
- Change: `単剤表示 / 複数薬まとめ` の切替背景を、免責バナーに近い黄色系グラデーションへ変更し、現場で気づきやすい見た目にした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Multi Med Selector Plan
- [x] Phase 1 Analyst: 複数薬まとめで本当に必要な操作が「表を読むこと」か「薬を選ぶこと」かを切り分ける
- [x] Phase 2 Critic: 表を主操作から外したときに、根拠確認や既存の表導線が失われないか確認する
- [x] Phase 3 Implementer: 上部チップ選択UIを追加し、個別表は確認用として折りたたみ表示へ下げる
- [x] Phase 4 Reviewer: 選択、個別解除、集計、表の開閉が既存集計と矛盾なく動くことを確認する

## Multi Med Selector Result
- Change: 複数薬まとめモードの主操作を、表内チェックではなく上部のカテゴリ別チップ選択へ移した。
- Change: 個別の行列表は `個別表で確認する` ボタンを押したときだけ表示する確認用UIへ下げ、通常時は集計結果に集中できるようにした。
- Change: 表を開いたときは選択済み薬に `選択中` マークだけを出し、選択責務をチップUIへ一元化した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Table Gap Bug Result
- Root cause: 表ヘッダーと1行目の間の白い空白は、sticky ヘッダー用の `--compat-head-height` が初回描画時にずれ、横スクロール時の再同期でだけ正しい高さに戻っていたため発生していた。
- Critic check: データ欠落や行高設定ではなく、横スクロールで解消することから sticky ヘッダーの同期タイミングの問題と判断した。
- Change: `scheduleCompatStickySync()` を追加し、表描画直後・表示切替直後・ページ切替直後に `requestAnimationFrame` と `setTimeout` を使って再同期するようにした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Multi Med Icon Result
- Change: `複数薬まとめ` セレクタの絵文字を `🧪` から `💊` に変更し、薬のまとまりを見る機能だと直感しやすい表現へ寄せた。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Multi Med Result Flow Result
- Root cause: 複数薬まとめの結果は更新されても、選択UIの直後に同じトーンで並んでいたため、結果エリアの存在に気づきにくかった。
- Critic check: ただ自動スクロールするだけだと選択作業を邪魔しうるので、結果エリア自体を常設しつつ、初回表示時だけ軽く誘導する方針にした。
- Change: `薬を選ぶ` と `処方のまとめ結果` を別パネルに分離し、結果側には専用見出し・バッジ・空状態メッセージを追加して役割を明確にした。
- Change: 2剤目到達時には結果パネルへ軽くスクロール+ハイライトし、その後の選択変更では結果パネルだけを更新強調するようにした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Multi Med Selected Badge Result
- Change: まとめモードで個別表を開いた時の `選択中` バッジを、チェックアイコン付き・濃いめのティール背景・枠線付きに変更し、薬名の横で見落としにくくした。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`

## Multi Med Prescription Context Result
- Change: 複数薬まとめの見出しと説明文を `今回の処方` / `この子の処方` ベースへ差し替え、患者側が「実際に出た薬を選んでいる」と想起しやすい文脈に寄せた。
- Change: `今回の処方に入っている薬` と `この子の処方で飲ませやすい候補` に、小さな補助アイコンと `今回の処方薬` ラベルを追加した。
- Test: `python3 tests/kusuri_navi_regression_check.py`
- Test: `node --check /tmp/kusuri-navi-review-check.js`
- Test: `node --check sw.js`
